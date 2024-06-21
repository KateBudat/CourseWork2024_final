from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from users.models import Material, Purchased_Material, Used_Material, Write_Off_Material, Supplier
from .forms import MaterialForm, SupplierForm, PurchasedMaterialForm, WriteOffMaterialForm, UsedMaterialForm
import template_views
from django.contrib import messages

from django.db import connection


def get_material_with_info():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_material_with_info()")
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return results


def materials(request):
    query = request.GET.get('query')

    material_info = get_material_with_info()
    purchased_materials = Purchased_Material.objects.all().order_by('-id_purchased_material')
    used_materials = Used_Material.objects.all().order_by('-id_used_material')
    write_off_materials = Write_Off_Material.objects.all().order_by('-id_write_off_material')
    suppliers = Supplier.objects.all().order_by('id_supplier')

    if query:
        material_info = [
            material for material in material_info
            if query.lower() in material['name_material'].lower() or
               query.lower() in material['brand'].lower() or
               query.lower() in material['barcode'].lower()
        ]
        purchased_materials = purchased_materials.filter(
            Q(material__name_material__icontains=query) |
            Q(material__brand__icontains=query) |
            Q(material__barcode__icontains=query)
        )
        used_materials = used_materials.filter(
            Q(material__name_material__icontains=query) |
            Q(material__brand__icontains=query) |
            Q(material__barcode__icontains=query)
        )
        write_off_materials = write_off_materials.filter(
            Q(purchased_material__material__name_material__icontains=query) |
            Q(purchased_material__material__brand__icontains=query) |
            Q(purchased_material__material__barcode__icontains=query)
        )
        suppliers = suppliers.filter(
            Q(company_name__icontains=query) |
            Q(contact_person__icontains=query) |
            Q(contact_telephone__icontains=query)
        )

    form = MaterialForm()

    context = {
        'material_info': material_info,
        'purchased_materials': purchased_materials,
        'used_materials': used_materials,
        'write_off_materials': write_off_materials,
        'suppliers': suppliers,
        'query': query,
        'form': form
    }

    return render(request, 'materials/materials.html', context)



@login_required
def add_material(request):
    return template_views.add_object(request, MaterialForm, 'materials/materials/add_material.html', 'materials')


@login_required
def edit_material(request, id_material):
    return template_views.edit_object(request, Material, MaterialForm, 'materials/materials/edit_material.html', 'materials',
                                      id_material)


@login_required
def delete_material(request, id_material):
    return template_views.delete_object(request, Material, id_material)


@login_required
def add_supplier(request):
    return template_views.add_object(request, SupplierForm, 'materials/suppliers/add_supplier.html', 'materials')


@login_required
def edit_supplier(request, id_supplier):
    return template_views.edit_object(request, Supplier, SupplierForm, 'materials/suppliers/edit_supplier.html', 'materials',
                                      id_supplier)


@login_required
def delete_supplier(request, id_supplier):
    return template_views.delete_object(request, Supplier, id_supplier, 'materials')

'''
@login_required
def add_purchased_material(request, id_material):
    material = get_object_or_404(Material, pk=id_material)
    if request.method == 'POST':
        form = PurchasedMaterialForm(request.POST)
        if form.is_valid():
            try:
                purchased_material = form.save(commit=False)
                purchased_material.material = material
                purchased_material.save()
                return redirect('materials')
            except Exception as e:
                messages.error(request, f"Виникла помилка: {str(e)}")
    else:
        form = PurchasedMaterialForm()
    return render(request, 'materials/add_purchased_material.html', {'form': form, 'material': material})

'''


@login_required
def add_template_material(request, model_class, form_class, id, redirect_page, template_name):
    item = get_object_or_404(model_class, pk=id)

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            try:
                new_item = form.save(commit=False)
                setattr(new_item, model_class._meta.model_name, item)
                new_item.save()
                return redirect(redirect_page)
            except Exception as e:
                messages.error(request, f"Виникла помилка: {str(e)}")
    else:
        form = form_class()

    return render(request, template_name, {'form': form, model_class._meta.model_name: item})


@login_required
def add_purchased_material(request, id_material):
    return add_template_material(
        request,
        Material,
        PurchasedMaterialForm,
        id_material,
        'materials',
        'materials/purchased/add_purchased_material.html'
    )



@login_required
def edit_purchased_material(request, id_purchased_material):
    purchased_material = get_object_or_404(Purchased_Material, pk=id_purchased_material)
    template_name = 'materials/purchased/edit_purchased_material.html'
    redirect_url = 'materials'

    extra_context = {
        'material': purchased_material.material,
        'purchased_material': purchased_material
    }

    return template_views.edit_object(request, Purchased_Material, PurchasedMaterialForm, template_name, redirect_url,
                                      id_purchased_material, extra_context)


@login_required
def delete_purchased_material(request, id_purchased_material):
    return template_views.delete_object(request, Purchased_Material, id_purchased_material, 'materials')


@login_required
def add_write_off_material(request, id_purchased_material):
    return add_template_material(
        request,
        Purchased_Material,
        WriteOffMaterialForm,
        id_purchased_material,
        'materials',
        'materials/write_off/add_write_off_material.html'
    )


@login_required
def edit_write_off_material(request, id_write_off_material):
    write_off_material = get_object_or_404(Write_Off_Material, pk=id_write_off_material)
    template_name = 'materials/write_off/edit_write_off_material.html'
    redirect_url = 'materials'

    extra_context = {
        'purchased_material': write_off_material.purchased_material,
        'write_off_material': write_off_material
    }

    return template_views.edit_object(request, Write_Off_Material, WriteOffMaterialForm, template_name, redirect_url,
                                      id_write_off_material, extra_context)


@login_required
def delete_write_off_material(request, id_write_off_material):
    return template_views.delete_object(request, Write_Off_Material, id_write_off_material, 'materials')


@login_required
def edit_used_material(request, id_used_material):
    used_material = get_object_or_404(Used_Material, pk=id_used_material)
    template_name = 'materials/used/edit_used_material.html'
    redirect_url = 'materials'

    extra_context = {
        'material': used_material.material,
        'registration': used_material.registration,
        'used_material': used_material
    }

    return template_views.edit_object(request, Used_Material, UsedMaterialForm, template_name, redirect_url,
                                      id_used_material, extra_context)


@login_required
def delete_used_material(request, id_used_material):
    return template_views.delete_object(request, Used_Material, id_used_material, 'materials')