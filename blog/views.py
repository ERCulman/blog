from django.shortcuts import render, get_object_or_404, redirect 
from django.utils import timezone
from .models import Post
from .forms import PostForm # Importar el formulario

def post_list(request):
    # QuerySet: filtra posts publicados (published_date <= ahora) y ordena 
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # Renderiza la plantilla, pasando los posts 
    return render(request, 'blog/post_list.html', {'posts': posts}) 

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST) # Construir formulario con datos POST 
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user # Establecer el autor como el usuario actual 
            post.published_date = timezone.now() # Publicar inmediatamente
            post.save() # Guardar en la base de datos 
            return redirect('post_detail', pk=post.pk) # Redirigir al detalle
    else:
        form = PostForm() # Crear formulario vacío para GET
    return render(request, 'blog/post_edit.html', {'form': form}) # Usamos la misma plantilla

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk) # Obtener el post existente
    if request.method == "POST":
        form = PostForm(request.POST, instance=post) # Pasamos la instancia y los datos POST
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post) # Pasamos la instancia para rellenar el formulario
    return render(request, 'blog/post_edit.html', {'form': form})
