<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>ToDo App</title>

		<link href="https://fonts.googleapis.com/css?family=Oswald" rel="stylesheet">

		<!-- Bootstrap CSS -->
		@vite('resources/css/bs/css/flatly.min.css')
		@vite('resources/css/app.css')
	</head>
	<body>

		<div class="container-fluid" id="wrapper">
			
			<div class="row">
				<div class="col-lg-4 col-lg-offset-4" id="content">
					<h2>WHAT DO YOU WANT TO DO TODAY?</h2>
					
					<form action="{{ route('todos.store') }}" method="POST" role="form">
						@csrf
						<div class="form-group">
							<div class="input-group">
							  <input type="text" name="text" class="form-control" placeholder="Enter todo e.g. Delete junk files" aria-label="Todo" aria-describedby="add-btn">
							  <span class="input-group-btn">
								  <button type="submit" class="btn btn-default" id="add-btn">ADD</button>
							  </span>
							</div>
						</div>
					</form>

					<div class="row t10">
						<div class="col-lg-12">
							<div class="btn-toolbar">
								<div class="btn-group">
									<a href="{{ route('todos.destroy_complete') }}"><button type="button" class="btn btn-warning">
										<i class="glyphicon glyphicon-trash"></i> DELETE COMPLETED
									</button></a>
								</div>
								<div class="btn-group">
									<a href="{{ route('todos.destroy_all') }}"><button type="button" class="btn btn-warning">
										<i class="glyphicon glyphicon-trash"></i> DELETE ALL
									</button></a>
								</div>
							</div>
						</div>
					</div>

					<ul class="list-group t20">
						@foreach($todos as $todo)
							@if($todo['complete'])
							<li class="list-group-item todo-completed">{{ $todo['text'] }}</li>
							@else
							<a href="{{ route('todos.complete', $todo['id']) }}"><li class="list-group-item">{{ $todo['text'] }}</li></a>
							@endif
						@endforeach
					</ul>
				</div>
			</div>

			<footer>
				<div class="row pad">
					<div class="col-lg-12 text-center">
						Copyright &copy; 2025 <strong>ToDo App</strong>
					</div>
				</div>
			</footer>
		</div>
	</body>
</html>