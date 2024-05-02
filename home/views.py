from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import uuid
from home.forms import CustomUserCreationForm
from home.models import Notes
from home.forms import NotesForm, ShareNotesForm


##! User


class LoginInterfaceView(LoginView):
    template_name = "home/login.html"
    authentication_form = AuthenticationForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("notes")
        return super().get(request, *args, **kwargs)


class SignupInterfaceView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "home/signup.html"
    success_url = reverse_lazy("signin")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])  # Ensure password encryption
        user.save()
        login(self.request, user)
        return super().form_valid(form)


class LogoutInterfaceView(LogoutView):
    next_page = reverse_lazy("notes")


##! Notes


class NotesDeleteView(DeleteView):
    model = Notes
    success_url = reverse_lazy("notes")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class NotesUpdateView(UpdateView):
    model = Notes
    success_url = reverse_lazy("notes")
    form_class = NotesForm


class NotesCreateView(CreateView):
    model = Notes
    success_url = reverse_lazy("notes")
    form_class = NotesForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = "notes"
    login_url = "/home"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.notes.all()
        else:
            return Notes.objects.none()


class NotesDetailView(DetailView):
    model = Notes
    context_object_name = "note"


##! Note Share


class NoteShareView(View):
    form_class = ShareNotesForm
    success_url = reverse_lazy("notes")

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            share_id = form.cleaned_data["shareid"]

            if not share_id:
                form.add_error("shareid", "Share ID cannot be empty.")
                return self.get(request, *args, **kwargs)

            queryset = self.get_queryset(share_id)

            for note in queryset:
                if note.user == request.user:
                    form.add_error(None, "You cannot share a note with yourself.")
                    return self.get(request, *args, **kwargs)

                try:
                    shared_note = Notes.objects.create(
                        title=note.title,
                        content=note.content,
                        user=request.user,
                        shareid=str(uuid.uuid4()),
                    )
                    shared_note.save()
                except Exception as e:
                    form.add_error(None, f"Error occurred while sharing note: {str(e)}")
                    return self.get(request, *args, **kwargs)

            return HttpResponseRedirect(self.success_url)

        return self.get(request, *args, **kwargs)

    def get_queryset(self, share_id):
        return Notes.objects.filter(shareid=share_id)


##! Home


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "MindScribe"
        context["description"] = (
            "MindScribe - Capture, Organize, and Share Your Thoughts Effortlessly. MindScribe is the ultimate "
            "note-taking and sharing web app, empowering you to record your ideas seamlessly, organize them "
            "effortlessly, and share them with ease. Whether you're brainstorming, planning, or reflecting, "
            "MindScribe simplifies the process, making note-taking a breeze. Get started today and unleash your "
            "creativity with MindScribe."
        )
        context["keywords"] = (
            "MindScribe, note-taking, sharing, web app, capture, organize, ideas, brainstorming, planning, "
            "reflection, creativity"
        )
        return context
