from django.contrib import admin

from .models import MPTP

# Register your models here.


@admin.register(MPTP)
class MPTPAdmin(admin.ModelAdmin):
    model = MPTP

    list_display = (
        "name",
        "itemdesc",
        "mptp_applies",
        "mptp",
        "date_added",
        "date_modified",
        "link",
    )

    list_display_links = (
        "link",
    )

    list_editable = (
        "name",
        "itemdesc",
        "mptp_applies",
        "mptp",
    )

    search_fields = (
        "name",
        "itemdesc",
    )

    save_on_top = True
