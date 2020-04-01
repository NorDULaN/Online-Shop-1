from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.template.defaultfilters import slugify
from django.http import JsonResponse
from django.urls import reverse
from django.views import View


from taggit.models import Tag
from .models import Manufacturer, Category, Product, MultipleImages
from .forms import (
        ManufacturerCreateForm,
        ManufacturerEditForm,
        CategoryModelForm,
        ProductCreateForm,
        ProductEditForm,
)

#  Tagging Class
class TaggedView(View):

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        if slug :
            tag = get_object_or_404(Tag, slug=slug)
            context = {
                'common_tags' : Product.tags.most_common()[:8],
                'query' : Product.objects.filter(tags=tag).order_by('name'),
            }
            return render(request, 'tag.html', context)
        context = {}
        return render(request, 'tag.html', context)


# Model Id Class
class ModelsObjectMixin(object):

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None :
            obj = get_object_or_404(self.model, id=id)
        return obj


# Ajax Classes
class GetTagsAjaxView(View):
    model = Product
    template_name = 'ajax/get_tags.html'

    def post(self, request, *args, **kwargs):
        if request.is_ajax :
            inputproduct = request.POST.get("inputproduct", None)
            if inputproduct :
                tags = Product.objects.filter(id = inputproduct).first().tags.all()
                all_tags = ""
                for tag in tags :
                    if all_tags == "" :
                         all_tags +=  tag.name
                    else:
                        all_tags += "," +  tag.name
                context = {
                        'tags' : all_tags,
                }
                return render(request, self.template_name, context)

        return JsonResponse({}, status = 400)


#  Product Classes
class ProductListView(ListView):
    template_name = "product/list.html"
    queryset = Product.objects.all()

class ProductDetailView(ModelsObjectMixin, DetailView):
    template_name = "product/detail.html"
    model = Product

class ProductCreateView(View):
    template_name = "product/create.html"

    def get(self, request, *args, **kwargs):
        form = ProductCreateForm()
        context = {
                'form' : form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.slug = slugify(new.name)
            multiple_images = request.FILES.getlist('multipleimages')
            new.save()
            form.save_m2m()
            for image in multiple_images:
                MultipleImages.objects.create(image=image, product_id=new.id)

            return redirect('main:product_detail', id=new.id)
        context = {
                'form' : form,
        }
        return render(request, self.template_name, context)

class ProductUpdateView(ModelsObjectMixin, View):
    template_name = "product/update.html"
    model = Product

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        form = ProductEditForm(instance=obj)
        context = {
                    'form' : form,
                    'object' : obj,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = ProductEditForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            new_name = form.cleaned_data.get('new_name', None)
            edit = form.save(commit=False)
            if new_name :
                edit.name = new_name
            edit.save()
            form.save_m2m()
            clear_images = form.cleaned_data.get("clear_images")
            if clear_images:
                MultipleImages.objects.filter(product_id=edit.id).delete()
            multiple_images = request.FILES.getlist('multipleimages')
            if multiple_images :
                for image in multiple_images:
                    MultipleImages.objects.create(image=image, product_id=edit.id)
            return redirect('main:product_detail', id=obj.id)
        context = {
                    'form' : form,
                    'object' : obj,
        }
        return render(request, self.template_name, context)

class ProductDeleteView(ModelsObjectMixin, View):
    template_name = "product/delete.html"
    model = Product

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        context = {
                    'object' : obj,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        context = {
                    'object' : obj,
        }
        if obj:
            obj.delete()
        return redirect('main:product_list')


#  Category Classes
class CategoryListView(ListView):
    template_name = 'category/list.html'
    queryset = Category.objects.all()

class CategoryCreateView(View):
    template_name = 'category/create.html'
    def get(self, request, *args, **kwargs):
        form = CategoryModelForm()
        context = {
                'form' : form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CategoryModelForm(request.POST)
        if form.is_valid():
            new = form.save()
        context = {
                'form' : form,
        }
        return render(request, self.template_name, context)

class CategoryUpdateView(ModelsObjectMixin, View):
    template_name = "category/update.html"
    model = Category

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        form = CategoryModelForm(instance=obj)
        context = {
                    'form' : form,
                    'object' : obj,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = CategoryModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
        context = {
                    'form' : form,
                    'object' : obj,
        }
        return render(request, self.template_name, context)

class CategoryDeleteView(ModelsObjectMixin, View):
    template_name = "category/delete.html"
    model = Category

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        context = {
                    'object' : obj,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        context = {
                    'object' : obj,
        }
        if obj:
            obj.delete()
        return redirect('main:category_list')


#  Manufacturer Classes
class ManufacturerListView(ListView):
    template_name = "manufacturer/list.html"
    queryset = Manufacturer.objects.all()

class ManufacturerDetailView(ModelsObjectMixin, DetailView):
    template_name = "manufacturer/detail.html"
    model = Manufacturer

class ManufacturerCreateView(View):
    template_name = "manufacturer/create.html"

    def get(self, request, *args, **kwargs):
        form = ManufacturerCreateForm()
        context = {
                'form' : form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ManufacturerCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save()
            return redirect('main:manufacturer_detail', id=new.id)
        context = {
                'form' : form,
        }
        return render(request, self.template_name, context)

class ManufacturerUpdateView(ModelsObjectMixin, View):
    template_name = "manufacturer/update.html"
    model = Manufacturer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        form = ManufacturerEditForm(instance=obj)
        context = {
                    'form' : form,
                    'object' : obj,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = ManufacturerEditForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            new_name = form.cleaned_data.get('new_name', None)
            new = form.save(commit=False)
            if new_name :
                new.name = new_name
            new.save()
            return redirect('main:manufacturer_detail', id=obj.id)
        context = {
                    'form' : form,
                    'object' : obj,
        }
        return render(request, self.template_name, context)

class ManufacturerDeleteView(ModelsObjectMixin, View):
    template_name = "manufacturer/delete.html"
    model = Manufacturer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        context = {
                    'object' : obj,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        context = {
                    'object' : obj,
        }
        if obj:
            obj.delete()
        return redirect('main:manufacturer_list')