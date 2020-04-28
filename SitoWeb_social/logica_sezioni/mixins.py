from django.contrib.auth.mixins import UserPassesTestMixin



#grazie a questo mixin solo lo staff potrà creare nuove sezioni fuori da admin
class StaffMixing(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
