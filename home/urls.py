from django.urls import path
import home.views as views


urlpatterns = [
    ##! Notes
    path("", views.NotesListView.as_view(), name="notes"),
    path("<int:pk>", views.NotesDetailView.as_view(), name="detail"),
    path("<int:pk>/edit", views.NotesUpdateView.as_view(), name="update"),
    path("<int:pk>/delete", views.NotesDeleteView.as_view(), name="delete"),
    path("new", views.NotesCreateView.as_view(), name="create"),
    ##! Account
    path("home", views.HomeView.as_view(), name="home"),
    path("login", views.LoginInterfaceView.as_view(), name="signin"),
    path("logout", views.LogoutInterfaceView.as_view(), name="logout"),
    path("signup", views.SignupInterfaceView.as_view(), name="signup"),
    ##! Note Share
    path("add/note", views.NoteShareView.as_view(), name="add"),
    # TODO
    # path("add/group", views.NoteShareGroupView.as_view(), name="addgroup"),
]
