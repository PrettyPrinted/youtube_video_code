<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Todo;

class TodoController extends Controller
{
    public function index() {
        $todos = Todo::all();
        return view('todos.index', ["todos" => $todos]);
    }

    public function store(Request $request) {
        $validated = $request->validate(["text" => 'required|string|max:40']);

        Todo::create($validated);

        return redirect()->route('todos.index');
    }

    public function update($id) {
        $todo = Todo::find($id);
        $todo->complete = true;
        $todo->save();

        return redirect()->route('todos.index');
    }

    public function destroyComplete() {
        Todo::where('complete', true)->delete();

        return redirect()->route('todos.index');
    }

    public function destroyAll() {
        Todo::query()->delete();

        return redirect()->route('todos.index');
    }
}
