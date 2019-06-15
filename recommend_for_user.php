<?php
    // get the q parameter from URL
    $q = $_REQUEST["q"];
    $str = file_get_contents('cf_recommend_result.json');
    $json = json_decode($str, true);

    for ($i = 0; $i < sizeof($json); $i++){
        $personId = $json[$i]['personId'];
        $recommendItems = $json[$i]['recommendItems'];
        if ($q == $personId){
            echo '<div class="container">';
            echo '<h1>You may like these :</h1>';
            echo '<div class="row">';
        // echo '<p style="color: brown;">User: '.$personId.'</p>';
            for ($j = 0; $j < 10; $j ++){
                echo '<div class="item col-md-2">';
                echo '<p style="color:red;">'.$recommendItems[$j].'</p>';
                echo '<img src="e.jpg">';
                echo '</div>';
            }
            echo '</div>';
            echo '</div>';
        }
    }
?>