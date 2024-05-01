from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    FormView,
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


class NoteShareView(FormView):
    template_name = "home/notes_list.html"
    form_class = ShareNotesForm
    success_url = "/"

    def form_valid(self, form):
        share_id = form.cleaned_data["shareid"]
        queryset = Notes.objects.filter(shareid=share_id)

        for note in queryset:
            shared_note = Notes.objects.create(
                title=note.title,
                content=note.content,
                user=self.request.user,
                shareid=str(uuid.uuid4()),
            )
            shared_note.save()

        return super().form_valid(form)


##! Home


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "MindScribe"
        context["description"] = (
            "MindScribe - Capture, Organize, and Share Your Thoughts Effortlessly. MindScribe is the ultimate note-taking and sharing web app, empowering you to record your ideas seamlessly, organize them effortlessly, and share them with ease. Whether you're brainstorming, planning, or reflecting, MindScribe simplifies the process, making note-taking a breeze. Get started today and unleash your creativity with MindScribe."
        )
        context["keywords"] = (
            "MindScribe, note-taking, sharing, web app, capture, organize, ideas, brainstorming, planning, reflection, creativity"
        )
        return context
