from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import generic
from django.views.decorators.http import require_POST
from .forms import UserCreateForm, CategoryForm, LoginForm, ToDoForm
from .models import ToDo, Category
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

# Create your views here.


"""一覧表示"""


def index(request):
    todo = ToDo.objects.order_by('-created_at')
    return render(request, 'todo/index.html',
                  {'todo': todo}
                  )


User = get_user_model()

"""ログイン、ログアウト"""


class Login(LoginView):
    form_class = LoginForm
    template_name = 'todo/login.html'


class Logout(LogoutView):
    template_name = 'todo/index.html'


"""カテゴリーリスト"""


def category_list(request):
    category_list = Category.objects.order_by('-title')
    context = {'category_list': category_list}
    return render(request, 'todo/category_list.html', context)


"""カテゴリー作成"""


@login_required
def create_category_input(request):
    if request.method == 'GET':
        category_form = CategoryForm(request.session.get('category_form_data'))
    else:
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            request.session['category_form_data'] = request.POST
            return redirect('todo:create_category_confirm')
    context = {
        'category_form': category_form,
    }
    return render(request, 'todo/create_category_input.html', context)


def create_category_confirm(request):
    """入力データの確認画面。"""
    # create_category_inputで入力したユーザー情報をセッションから取り出す。
    session_form_data = request.session.get('category_form_data')
    if session_form_data is None:
        # セッション切れや、セッションが空でURL直接入力したら入力画面にリダイレクト。
        return redirect('todo:create_category_input')
    context = {
        'category_form': CategoryForm(session_form_data)
    }
    return render(request, 'todo/create_category_confirm.html', context)


@require_POST
def create_category_save(request):
    session_form_data = request.session.pop('category_form_data', None)
    if session_form_data is None:
        return redirect('todo:create_category_input')
    form = CategoryForm(session_form_data)
    if form.is_valid():
        form.save()
        return redirect('todo:index')


"""
class UserList(generic.ListView):
    """"""ユーザーを一覧表示。""""""
    # デフォルトUserだと、authアプリケーションのuser_list.htmlを探すため、明示的に指定する。
    template_name = 'todo/user_list.html'
    model = User
"""


def user_data_input(request):
    """新規ユーザー情報の入力。"""
    # 一覧表示からの遷移や、確認画面から戻るリンクを押したときはここ。
    if request.method == 'GET':
        # セッションに入力途中のデータがあればそれを使う。
        form = UserCreateForm(request.session.get('form_data'))
    else:
        form = UserCreateForm(request.POST)
        if form.is_valid():
            # 入力後の送信ボタンでここ。セッションに入力データを格納する。
            request.session['form_data'] = request.POST
            return redirect('todo:user_data_confirm')

    context = {
        'form': form
    }
    return render(request, 'todo/user_data_input.html', context)


def user_data_confirm(request):
    """入力データの確認画面。"""
    # user_data_inputで入力したユーザー情報をセッションから取り出す。
    session_form_data = request.session.get('form_data')
    if session_form_data is None:
        # セッション切れや、セッションが空でURL直接入力したら入力画面にリダイレクト。
        return redirect('todo:user_data_input_input')

    context = {
        'form': UserCreateForm(session_form_data)
    }
    return render(request, 'todo/user_data_confirm.html', context)


@require_POST
def user_data_create(request):
    """ユーザーを作成する。"""
    # user_data_inputで入力したユーザー情報をセッションから取り出す。
    # ユーザー作成後は、セッションを空にしたいのでpopメソッドで取り出す。
    session_form_data = request.session.pop('form_data', None)
    if session_form_data is None:
        # ここにはPOSTメソッドで、かつセッションに入力データがなかった場合だけ。
        # セッション切れや、不正なアクセス対策。
        return redirect('todo:user_data_input')

    form = UserCreateForm(session_form_data)
    if form.is_valid():
        form.save()
        return redirect('todo:user_list')
    # is_validに通過したデータだけセッションに格納しているので、ここ以降の処理は基本的には通らない。
    context = {
        'form': form
    }
    return render(request, 'todo/user_data_input.html', context)


"""ToDoを作る"""


@login_required
def create_todo_input(request):
    if request.method == 'GET':
        todo_form = ToDoForm(request.session.get('todo_form_data', None))
    else:
        todo_form = ToDoForm(request.POST)
        if todo_form.is_valid():
            request.session['todo_form_data'] = request.POST
            return redirect('todo:create_todo_confirm')
    context = {
        'todo_form': todo_form
    }
    return render(request, 'todo/create_todo_input.html', context)


def create_todo_confirm(request):
    session_form_data = request.session.get('todo_form_data')
    if session_form_data is None:
        return redirect('todo:create_todo_input')
    category_name = Category.objects.get(pk=session_form_data['category'])
    context = {
        'form': ToDoForm(session_form_data),
        'category_name': category_name,
    }
    return render(request, 'todo/create_todo_confirm.html', context)


@require_POST
def create_todo_save(request):
    session_form_data = request.session.pop('todo_form_data')
    if session_form_data is None:
        return redirect('todo:create_todo_input')
    form = ToDoForm(session_form_data)
    if form.is_valid():
        form.save()
        return redirect('todo:index')


"カテゴリー別ToDoリスト"


def todo_list(request, pk):
    todos = ToDo.objects.filter(category_id__exact=pk)
    if todos is None:
        return redirect('todo:index')
    context = {
        'todos': todos
    }
    return render(request, 'todo/todo_list.html', context)

