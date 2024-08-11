from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from users.decorators import role_required


@role_required(allowed_roles=['master_user', 'owner_user', 'administrator_user'])
def add_object(request, form_class, template_name, redirect_url, extra_context=None):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect(redirect_url)
            except Exception as e:
                messages.error(request, f"Виникла помилка: {str(e)}")
        else:
            messages.error(request, "Форма не є дійсною. Перевірте введені дані.")
    else:
        form = form_class()
    context = {'form': form}
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template_name, context)


@role_required(allowed_roles=['master_user', 'owner_user', 'administrator_user'])
def edit_object(request, model, form_class, template_name, redirect_url, id, extra_context=None):
    obj = get_object_or_404(model, pk=id)
    if request.method == 'POST':
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Дані оновлено!")
                return redirect(redirect_url)
            except ObjectDoesNotExist:
                messages.error(request, "Об'єкт не існує")
            except Exception as e:
                messages.error(request, f"Виникла помилка: {str(e)}")
        else:
            messages.error(request, "Форма не є дійсною. Перевірте введені дані.")
    else:
        form = form_class(instance=obj)

    context = {'form': form}
    if extra_context:
        context.update(extra_context)

    return render(request, template_name, context)


@role_required(allowed_roles=['master_user', 'owner_user', 'administrator_user'])
def delete_object(request, model, id, redirect_url=None):
    model_name = model._meta.model_name
    try:
        obj = model.objects.get(pk=id)
        obj.delete()
        messages.success(request, f"{model_name.capitalize()} успішно видалено!")
    except ObjectDoesNotExist:
        messages.error(request, "Об'єкт не існує")
    except Exception as e:
        messages.error(request, f"Виникла помилка: {str(e)}")

    if redirect_url:
        return redirect(redirect_url)
    return redirect(f'{model_name}s')
