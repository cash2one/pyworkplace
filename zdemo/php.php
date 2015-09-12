<?php
$data = array(
  'email'   => 'i@imcfy.com',
  'password'   => '000000',
  'client_id'  => '7781809591'
);
$api_url='https://apis.chinabrands.com/app_login_api.php';
$client_secret='8784c11b8723b92ed24b76c84a831315';

$json_data = json_encode($data);
$signature_string = md5($json_data.$client_secret); //签名数据

// echo $signature_string.'</br>';


$post_data = 'signature='.$signature_string.'&data='.urlencode($json_data);
// echo $json_data.'</br>';
// echo urlencode($json_data).'</br>';
// echo $post_data ;
$curl = curl_init($api_url);
curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 1);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($curl, CURLOPT_POST, 1);
curl_setopt($curl, CURLOPT_POSTFIELDS, $post_data);
$result = curl_exec($curl); //返回结果
// echo  $result;
curl_close($curl); 
?>