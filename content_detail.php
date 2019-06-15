<?php
$q = $_REQUEST["q"];
$str = file_get_contents('content_detail.json');
$json = json_decode($str, true);

for($i = 0; $i < sizeof($json); $i++){
    $contentId = $json[$i]['contentId'];
    if($q == $contentId){
        echo '
        <div class="modal-header">
            <h4 class="modal-title">'.$json[$i]['title'].'</h4>
        </div>
        <div class="modal-body">
            <p>Author: <b>'.$json[$i]['authorPersonId'].'</b><span> in:</span><i>'.$json[$i]['timestamp'].'</i></p>
            <p>link: <i>'.$json[$i]['url'].'</i></p>
            <p>'.$json[$i]['text'].'</p>
        </div>';
        break;  
    }
}
?>