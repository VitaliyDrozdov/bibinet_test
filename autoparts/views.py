import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from .models import Mark, Model, Part


class ModelList(ListView):
    model = Model
    queryset = Model.objects.filter(is_visible=True)
    template_name = "model_list.html"
    paginate_by = 10


class MarkList(ListView):
    model = Mark
    queryset = Mark.objects.filter(is_visible=True)
    template_name = "mark_list.html"
    paginate_by = 10


class PartListView(ListView):
    model = Part
    queryset = Part.objects.all()
    template_name = "part_list.html"
    paginate_by = 10
    context_object_name = "parts"


@method_decorator(csrf_exempt, name="dispatch")
class PartSearchView(View):
    template_name = "search_part.html"

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        filters = {
            "is_visible": True,
        }
        mark_list = data.get("mark_list")
        mark_name = data.get("mark_name")
        part_name = data.get("part_name")
        params = data.get("params", {})
        price_gte = data.get("price_gte")
        price_lte = data.get("price_lte")

        if mark_list:
            filters["mark_id__in"] = mark_list
        elif mark_name:
            filters["mark__name__iexact"] = mark_name

        if part_name:
            filters["name__icontains"] = part_name.capitalize()
        if params:
            for key, value in params.items():
                if value is not None:
                    filters[f"json_data__{key}"] = value

        if price_gte is not None:
            filters["price__gte"] = price_gte

        if price_lte is not None:
            filters["price__lte"] = price_lte

        parts = Part.objects.filter(**filters).select_related("mark", "model")

        paginator = Paginator(parts, 10)
        page_number = data.get("page", 1)
        page_obj = paginator.get_page(page_number)

        response_data = {
            "response": list(
                page_obj.object_list.values(
                    "mark__id",
                    "mark__name",
                    "mark__producer_country_name",
                    "model__id",
                    "model__name",
                    "name",
                    "json_data",
                    "price",
                )
            ),
            "count": paginator.count,
            "summ": sum(part.price for part in page_obj.object_list),
        }
        return JsonResponse(response_data, safe=False)
