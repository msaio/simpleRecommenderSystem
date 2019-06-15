<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Home</title>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">

    <!-- jQuery library -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
    <!-- <script src="onItemClick.js"></script> -->
    <!-- Popper JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>

    <!-- Latest compiled JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>

</head>
<body>     
    <div class="container col-md-4" id="simpleLogin">
        <div class="form-group">
            <label for="inputUser">Login as user</label>
            <select id="inputUser" class="form-control">
                <option selected>Choose...</option>
                <?php
                $str = file_get_contents('personId.json');
                $json = json_decode($str, true);
                $user = $json["personId"];
                foreach($user as $id){
                    echo "<option>";
                    echo $id;
                    echo "</option>";
                }
                ?>
            </select>
            <script>
                $(document).ready(function(){
                    $("#inputUser").change(function(){
                        const selectedUser = $(this).children("option:selected").val();
                        // alert("You have selected user - " + selectedUser);
                        $.ajax("recommend_for_user.php?q="+selectedUser, {success: function(result){
                            $("#recommendForUser").html(result);
                        }});
                    });
                    $("#ppItems").load("ppitems.php");
                });
            </script>
        </div>
    </div>
    

    <div id="recommendForUser" style="background-color:yellow;"></div>
    <div id="ppItems" style="background-color:pink;"></div>
    
    <div id="contentDetail">
        <div class="modal fade" id="myModal" role="dialog">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <script>
                        $("body").on("click", "div.item",function(){
                            $(this).attr("data-toggle", "modal");
                            $(this).attr("data-target", "#myModal");
                            console.log("1");
                            const selectedItem = $(this).children("p:first").text();
                            $.ajax("content_detail.php?q="+selectedItem, {success: function(result){
                                $(".modal-content").html(result);
                            }});
                        });
                    </script>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>