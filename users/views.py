from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic

from .forms import UserRegisterForm, UserUpdateForm, ContactForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}.')
            return redirect('user-login')

    else: 
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def account(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account information successfully updated!')
            return redirect('user-account')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'users/account.html', context)

#class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
#    template_name = 'users/account.html'
#    form_class = UserUpdateForm
#
#    def test_func(self):
#        if self.request.user.username == self.kwargs.get('username'):
#            return True
#        return False
#    
#    def get_object(self, queryset=None): 
#            return self.request.user.username
#
#    def form_valid(self, request, form):
#            clean = form.cleaned_data 
#            context = {}        
#            self.object = context.save(clean) 
#            messages.success(request, f'Account information successfully updated!')
#            return super(AccountUpdateView, self).form_valid(form)    #redirect('user-account', kwargs={'username': self.request.user.username})

class ContactFormView(generic.FormView):
    form_class = ContactForm
    template_name = "users/contact_us.html"
    success_url = reverse_lazy("user-contact")

    def form_valid(self, form):
        messages.success(self.request, 
                        f"""
                            '{form.cleaned_data.get('subject').strip()}' has been sent, we'll get back to you as soon as possible.
                        """)
        form.send_email()
        return super().form_valid(form)  