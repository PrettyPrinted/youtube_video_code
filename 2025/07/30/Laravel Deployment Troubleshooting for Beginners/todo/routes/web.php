<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\TodoController;

Route::get('/', [TodoController::class, 'index'])->name('todos.index');

Route::post('/store', [TodoController::class, 'store'])->name('todos.store');

Route::get('/complete/{id}', [TodoController::class, 'update'])->name('todos.complete');

Route::get('/delete_complete', [TodoController::class, 'destroyComplete'])->name('todos.destroy_complete');

Route::get('/delete_all', [TodoController::class, 'destroyAll'])->name('todos.destroy_all');
