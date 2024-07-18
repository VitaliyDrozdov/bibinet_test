from django.urls import path

from autoparts.views import MarkList, ModelList, PartListView, PartSearchView

app_name = "autoparts"

urlpatterns = [
    path("mark/", MarkList.as_view(), name="mark_list"),
    path("model/", ModelList.as_view(), name="model_list"),
    path("search/part/", PartSearchView.as_view(), name="search_part"),
    path("parts/", PartListView.as_view(), name="part_list"),
]
