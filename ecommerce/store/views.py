from django.shortcuts import render, redirect
from .models import Product
from django.contrib import messages
from .forms import NewUserForm, UserForm, ProfileForm, VoteForm
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

def homepage(request):
	if request.method == "POST":
		product_id = request.POST['product_pk'] # why admin use get instead of this line
		product = Product.objects.get(id = product_id)
		request.user.profile.products.add(product)
		messages.success(request,(f'{product} added to watch list.'))
		return redirect ('store:homepage')	
	products = Product.objects.all()
	#new_posts = Article.objects.all().order_by('-article_published')[:4]
	#featured = Article.objects.filter(article_tags__tag_name='Featured')[:3]
	#most_recent = new_posts.first()
	return render(request=request, template_name="store/store.html", context={'products':products})
	
	
def products(request):
	if request.method == "POST":
		product_id = request.POST["product_pk"]
		product = Product.objects.get(id = product_id)
		request.user.profile.products.add(product)
		messages.success(request,(f'{product} added to watch list.'))
		return redirect ('store:products')
	else:
	 #print(request.GET.get('search-area'))
	 
	 if request.GET.get('type'):
	  products=Product.objects.filter(category=request.GET[
	 'type'])
	  
	 else:
	  products = Product.objects.all()
	paginator = Paginator(products, 2)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	vote_form = VoteForm()
	return render(request = request, template_name="store/products.html", context = { "page_obj":page_obj, "vote_form":vote_form})
	
	
def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("store:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="store/register.html", context={"form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("store:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="store/login.html", context={"form":form})
	
def logout_request(request):
  logout(request)
  return redirect('/')
	
def userpage(request):
	if request.method == "POST":
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, instance=request.user.profile)
		if user_form.is_valid():
		    user_form.save()
		    messages.success(request,('Your profile was successfully updated!'))
		elif profile_form.is_valid():
		    profile=profile_form.save()
		    messages.success(request,('Your wishlist was successfully updated!'))
		else:
		    messages.error(request,('Unable to complete request'))
		return redirect ("store:userpage")
	user_form = UserForm(instance=request.user)
	profile_form = ProfileForm(instance=request.user.profile)
	return render(request = request, template_name ="store/user.html", context = {"user":request.user, 
		"user_form": user_form, "profile_form": profile_form })
   