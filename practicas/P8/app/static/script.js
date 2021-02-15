// Botones dia noche

$(document).ready(function(){

    $("#dia").click(function(){
        $("#dia").removeClass("btn-primary");
        $("#dia").addClass("btn-outline-primary");
        $("#noche").removeClass("btn-outline-dark");
        $("#noche").addClass("btn-dark");
        //cambiando el color de main
        $("main, main *, body").removeClass("bg-secondary");
        $("main, main *, body").addClass("bg-while");
        //cambiando el color de aside y footer
        $("footer, aside, aside *").removeClass("bg-dark");
        $("footer, aside, aside *").addClass("bg-light");
        //cambiando el color de letra
        $("footer *, aside *").addClass("text-dark");
        $("footer *, aside *").removeClass("text-while");
    });
    $("#noche").click(function(){
        $("#noche").removeClass("btn-dark");
        $("#noche").addClass("btn-outline-dark");
        $("#dia").removeClass("btn-outline-primary");
        $("#dia").addClass("btn-primary");
        //cambiando el color de main
        $("main, main *, body").removeClass("bg-white");
        $("main, main *, body").addClass("bg-secondary");
        //cambiando el color de aside y footer
        $("footer, aside, aside * ").removeClass("bg-light");
        $("footer, aside, aside *").addClass("bg-dark");
        //cambiando el color de letra
        $("footer *, aside *").addClass("text-white");
        $("footer *, aside *").removeClass("text-dark");
    });
});

$( document ).ready(function(){
    let htmlString = ''
    var $bloqueFilm = $('#bloqueFilm')
    $.ajax({
      type:'GET',
      url: '/api/films',
      success:function(films){
        $.each(films, function(i, film){
        htmlString += `<tr class="buscame" id="${film._id}">
        <td >
            <ul class="list-group bg-light">
                    <li class="list-group-item"><strong>Id:</strong> ${film._id}</li>
                    <li class="list-group-item"><strong>Actors:</strong>
                        <ul class="list-group ">`
                        $.each(film.Actors,function(j,actor){
                            htmlString += `<li class="list-group ">Apellido: ${actor["Last name"]}, Nombre: ${actor["First name"]}, id: ${actor.actorId}</li>`
                        });
        htmlString+=   `</ul>
                    </li>
                    <li class="list-group-item"><strong>Category:</strong> ${film.Category} </li>
                    <li class="list-group-item"><strong>Description:</strong> ${film.Description} </li>
                    <li class="list-group-item"><strong>Length:</strong> ${film.Length} </li>
                    <li class="list-group-item"><strong>Rental Duration:</strong> ${film.Rating} </li>
                    <li class="list-group-item"><strong>Rental Duration:</strong> ${film["Rental Duration"]} </li>
                    <li class="list-group-item"><strong>Replacement Cost:</strong> ${film["Replacement Cost"]} </li>
                    <li class="list-group-item"><strong>Special Features:</strong> ${film["Special Features"]} </li>
                    <li class="list-group-item"><strong>Title:</strong> ${film.Title} </li>
            </ul>
        </td>
        <td>
            <form action="/editar_films" method="POST">
                <div class="form-group">
                    <input type="hidden" name="editar" value="${film.Title}">
                    <input type="submit" class="btn btn-lg btn-warning"  value="Editar" >
                </div>
            </form>
            <div class="form-group">
                <input type="submit" class="btn btn-lg btn-danger" onclick="Borrar('${film.Title}')" value="Borrar" >
            </div>
        </td>
        </tr>`

        });
        $bloqueFilm.append(htmlString)
      }
    });
  });

$(function () {
// evento para cuando cambia el valor introducido en un <input id="buscar" $gt;
    $('#buscar').keyup(function(){
    let value = $(this).val()
    var $buscame = $('.buscame')
    console.log(value)

    if(value != ""){
        $.ajax({
            type : 'GET',
            url: '/api/films/' + value,
            success:function(films){
                $buscame.hide()
                $.each(films,function(i,film){
                    console.log(film.Title)
                    $("#" + film._id).show()
                })
            }
        })
    }else{
        $buscame.show()
    }
    })
});

// Click en el botón borrar
function Borrar(value) {
    // Para poner otra vez funciones jQuery en el DOM actual
    $(function () {
    console.log(value)
        var $id
        $.ajax({
            type : 'GET',
            url: '/api/films/' + value,
            success:function(films){
                $.each(films,function(i,film){
                    console.log(film.Title)
                    $id = film._id
                })
            }
        })
        $.ajax({
            url: '/api/films/' + value,
            type:'DELETE',
            success:function(result){
                $("#" + $id).remove()
            }
        });
    });
}