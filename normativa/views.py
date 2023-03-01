import datetime
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q
from .models import Circular
from .forms import SearchForm


def circular(request, year=None, month=None, todas_circulares=None):
    ''''''

    qs = False
    formatted_date = ''
    before_last_year = str(int(timezone.now().strftime("%Y")) - 2)
    last_year = str(int(timezone.now().strftime("%Y")) - 1)
    current_year = timezone.now().strftime("%Y")
    form_search = SearchForm()

    # todos las circulares año curso
    object_list = Circular.objects.filter(publish__year=current_year)

    if todas_circulares:
        object_list = Circular.objects.all()

    if year and month:
        object_list = Circular.objects.filter(
            publish__year=int(year), publish__month=int(month)
        )
        qs = True
        formatted_date = datetime.datetime(year, month, 17).strftime("%B %Y")

    # object_list = Circular.objects.all()

    paginator = Paginator(object_list, 10)  # circulares(objects) in each page
    page = request.GET.get("page")
    try:
        circulares = paginator.page(page)  # todos los objetos de una página

    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        circulares = paginator.page(1)

    except EmptyPage:
        # if pages is out of range deliver las page of results
        circulares = paginator.page(paginator.num_pages)

    return render(
        request,
        "normativa/circular_list.html",
        {
            "circulares": circulares,
            "page": page,
            'current_year': current_year,
            'last_year': last_year,
            'before_last_year': before_last_year,
            'qs': qs,
            'formatted_date': formatted_date,
            'todas_las_circulares': todas_circulares,
            'form': form_search
        },
    )


def circular_search(request):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            # Búsqueda
            results = set(
                Circular.objects.filter(
                    Q(title__icontains=query) | Q(search_date__icontains=query)
                )
            )
            print(results)

    return render(
        request, "normativa/search.html", {"query": query, "form": form, "results": results}
    )


# def historico_circulares(request, year=None, month=None, todas_circulares=None):
#     '''Vamos a obtener las circulares de los dos años anteriores al año en curso'''

#     year_month_circulares = None
#     get_all_circulares = False
#     qs = False
#     formatted_date = ''
#     before_last_year = str(int(timezone.now().strftime("%Y")) - 2)
#     last_year = str(int(timezone.now().strftime("%Y")) - 1)
#     current_year = timezone.now().strftime("%Y")

#     if todas_circulares:
#         get_all_circulares = Circular.objects.all()

#     if year and month:
#         year_month_circulares = Circular.objects.filter(
#             start__year=int(year), start__month=int(month)
#         )
#         qs = True
#         formatted_date = datetime.datetime(year, month, 17).strftime("%B %Y")

#     # todos las circulares cuya fecha de comienzo es el mes actual del año curso
#     current_year_circulares = Circular.objects.filter(start__year=current_year)

#     return render(
#         request,
#         "core/circular_list.html",
#         {
#             "current_year_circulares": current_year_circulares,
#             'current_year': current_year,
#             'last_year': last_year,
#             'before_last_year': before_last_year,
#             'year_month_circulares': year_month_circulares,
#             'qs': qs,
#             'formatted_date': formatted_date,
#             'get_all_circulares': get_all_circulares,
#         },
#     )
