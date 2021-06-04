from django.contrib import admin
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import escape
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.models import User
from .models import *


# class AdminPhoto(admin.ModelAdmin):
#     list_display = ['id', 'user', 'image', 'time']

class AdminCate(admin.ModelAdmin):
    list_display = ['id', 'name', 'time']

class AdminLog(admin.ModelAdmin):
    list_display = ['id', 'ip', 'action', 'login', 'time']

class AdminAlbum(admin.ModelAdmin):
    list_display = ['id', 'name', 'tags', 'time']

class AdminPhoto(admin.ModelAdmin):
    list_display = ['id', 'name', 'admin_photo', 'category', 'album', 'time']

    actions_selection_counter = True
    #actions_on_bottom = False
    #actions_on_top = True

    # fields = ('name', 'title','description', 'image', 'admin_photo')
    
    list_display_links=[
        'name',
        'album'
    ]
    list_filter = [
        'name',
        'album',
        'category',
        'time'
    ]
    # date_hierarchy = 'time'
    
    readonly_fields = ('time','admin_photo')

class AdminLocation(admin.ModelAdmin):
    list_display = ['id', 'name', 'time']

class AdminContact(admin.ModelAdmin):
    list_display = ['id', 'name', 'mail', 'time']

class AdminStaff(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'instagram', 'image', 'time']



# admin.site.register(Insta_Photo, AdminPhoto)
admin.site.register(Category, AdminCate)
admin.site.register(Log, AdminLog)
admin.site.register(Location, AdminLocation)
admin.site.register(Album, AdminAlbum)
admin.site.register(Photo, AdminPhoto)
admin.site.register(Contact, AdminContact)
admin.site.register(Staff_user, AdminStaff)















# Log Entry Do Not Edit

action_names = {
    ADDITION: 'Addition',
    CHANGE:   'Change',
    DELETION: 'Deletion',
}

class FilterBase(admin.SimpleListFilter):
    def queryset(self, request, queryset):
        if self.value():
            dictionary = dict(((self.parameter_name, self.value()),))
            return queryset.filter(**dictionary)

class ActionFilter(FilterBase):
    title = 'action'
    parameter_name = 'action_flag'
    def lookups(self, request, model_admin):
        return action_names.items()

class UserFilter(FilterBase):
    """Use this filter to only show current users, who appear in the log."""
    title = 'user'
    parameter_name = 'user_id'
    def lookups(self, request, model_admin):
        return tuple((u.id, u.username)
            for u in User.objects.filter(pk__in =
                LogEntry.objects.values_list('user_id').distinct())
        )

class AdminFilter(UserFilter):
    """Use this filter to only show current Superusers."""
    title = 'admin'
    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(is_superuser=True))

class StaffFilter(UserFilter):
    """Use this filter to only show current Staff members."""
    title = 'staff'
    def lookups(self, request, model_admin):
        return tuple((u.id, u.username) for u in User.objects.filter(is_staff=True))

class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

    # readonly_fields = LogEntry._meta.get_all_field_names()
    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.get_fields()]

    list_filter = [
        UserFilter,
        ActionFilter,
        'content_type',
        # 'user',
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]


    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'action_description',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        ct = obj.content_type
        repr_ = escape(obj.object_repr)
        try:
            href = reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id])
            link = u'<a href="%s">%s</a>' % (href, repr_)
        except NoReverseMatch:
            link = repr_
        return link if obj.action_flag != DELETION else repr_
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')

    def action_description(self, obj):
        return action_names[obj.action_flag]
    action_description.short_description = 'Action'


admin.site.register(LogEntry, LogEntryAdmin)

