# views.py
# login view with form cleaned_data
class UserLoginView(View):
    template_name = 'login.html'

    @method_decorator(anonymous_required)
    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated :
            return redirect('/')
        form = UserLoginForm()
        context = {
                'form' : form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(self.request, username=username, password=password)
            if user is not None:
                login(self.request, user)
                return redirect('/')
        else:
            context = {
                    'form' : form,
            }
        return render(request, self.template_name, context)

# forms.py

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, label=_("Username"))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(), label=_("Password"))

    def clean_username(self):
        cleaned_data = super().clean()
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username):
            raise forms.ValidationError(_("Username Does not Exist"))
        return username

    def clean_password(self):
        cleaned_data = super().clean()
        password = self.cleaned_data['password']
        if 'username' in self.cleaned_data :
            if not authenticate(username=self.cleaned_data['username'], password=password):
                raise forms.ValidationError(_("Invalid Password"))
        return password
