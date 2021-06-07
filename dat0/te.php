<?php
ignore_user_abort(1);
error_reporting(0);
header("Content-Type: text/html; charset=utf-8");

  $cat = array();
  $xml = new XMLReader();
  $xml->open('./yml - t2.xml');
    
  while($xml->read() && $xml->name !== 'category');
    while($xml->name === 'category'){
      $node = new SimpleXMLElement($xml->readOuterXML());
      $id = +$xml->getAttribute("id");
      $name = ''. $node;
      
      $cat[$id] = $name;
      
    $xml->next('category');
    }
  $xml->close();			

//////////////////////////////

  $xml = new XMLReader();
  $xml->open('./yml - Kopie.xml');	
    
  $allparams = array();
  $idparams = array();
  while($xml->read() && $xml->name !== 'offer');
    while($xml->name === 'offer'){
      $node = new SimpleXMLElement($xml->readOuterXML());	
      $id = +$xml->getAttribute("id");
      
      foreach ($node->param as $param){
        $name = ''. $param['name'];
        $value = ''. $param;
        $allparams[] = ''. $param['name'];				
        $idparams[$id][$name] = $value;
      }				
    $xml->next('offer');
    }
  $xml->close();
  
  $allparams = array_unique($allparams);
  sort($allparams);

//////////////////////////////

  $xml = new XMLReader();
  $xml->open('./yml - Kopie.xml');
  $flag = true;	
  while($xml->read() && $xml->name !== 'offer');
    while($xml->name === 'offer'){
      $node = new SimpleXMLElement($xml->readOuterXML());
      
      $id = $xml->getAttribute("id");
      $available = $xml->getAttribute("available");
      $url = $node->url;
      $price = $node->price;
      $currencyId = $node->currencyId;
      $delivery = $node->delivery;
      $local_delivery_cost = $node->local_delivery_cost;
      $typePrefix = $node->typePrefix;
      $vendor = $node->vendor;
      $vendorCode = $node->vendorCode;
      $model = $node->model;
      $description = $node->description;
      $cpa = $node->cpa;
      $weight = $node->weight;
      $pickup = $node->pickup;
      $c = +$node->categoryId;
      $category = $cat[$c];
      
      $picture = '';
      foreach ($node->picture as $pic){
        $picture .= $pic .' ';			   
      }					
      
      if($flag){
        $str = '"id";"Наличие";"url товара";"Цена";"Валюта";"Доставка";"Цена доставки";"Тип";"Производитель";"Код производителя";"Модель";"Описание";"Заказ на маркете";"Вес";"url картинки";"Самовывоз";"Категория";';
        $j = count($allparams);
        while($j-- > 0){
          $str .= '"'. $allparams[$j] .'";';
        }
        $str .= PHP_EOL;
        $str = mb_convert_encoding ($str ,"Windows-1251" , "UTF-8" );			
        $path = fopen("out.csv", "a+");
        fwrite($path, $str);
        fclose($path);
        $flag = false;
      }
      
      $params = '';
      $j = count($allparams);
      while($j-- > 0){				
        $params .= '"'. $idparams[$id][$allparams[$j]] .'";';			
      }		
      
      $str = '"'. $id .'";';
      $str .= '"'. $available .'";';
      $str .= '"'. $url .'";';
      $str .= '"'. $price .'";';
      $str .= '"'. $currencyId .'";';
      $str .= '"'. $delivery .'";';
      $str .= '"'. $local_delivery_cost .'";';
      $str .= '"'. $typePrefix .'";';
      $str .= '"'. $vendor .'";';
      $str .= '"'. $vendorCode .'";';
      $str .= '"'. $model .'";';
      $str .= '"'. $description .'";';
      $str .= '"'. $cpa .'";';
      $str .= '"'. $weight .'";';			
      $str .= '"'. $picture .'";';
      $str .= '"'. $pickup .'";';
      $str .= '"'. $category .'";';
      $str .= $params;
      $str .= PHP_EOL;
      
      $str = mb_convert_encoding ($str ,"Windows-1251" , "UTF-8" );			
      $path = fopen("out.csv", "a+");
      fwrite($path, $str);
      fclose($path);			
      
    $xml->next('offer');
    }
  $xml->close();
gc_enable();
echo 'ok';
?>
