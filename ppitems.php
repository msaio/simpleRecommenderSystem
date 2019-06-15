<?php
    $str = file_get_contents("popularity_items.json");
    $json = json_decode($str, true);
    echo '<div class="container">';
    echo '<h2>Top 6 popularity items with rates:</h2>';
    echo '<div class="row">';
    for ($i = 0; $i < 6; $i++){
        $contentId = $json[$i]['contentId'];
        $rate = $json[$i]['eventStrength'];
        echo '<div class="item col-md-2">';
        echo '<p style="color:blue;">'.$contentId.'</p>';
        echo '<p>has rate: '    .$rate.'</p>';
        echo '<img src="p.jpg">';
        echo '<hr>';
        echo '</div>';
    }
    echo '</div>';
    echo '</div>';
?>