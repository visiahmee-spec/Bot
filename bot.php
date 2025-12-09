<?php
// ============================================
// AHMED TELEGRAM BOT - COMPLETE SYSTEM
// ============================================

$botToken = "7497151281:AAHQLlqAR3dMcosj3uevoK3_E6PdHnM3inw";
$website = "https://api.telegram.org/bot".$botToken;

// رسائل النظام
$validauth = urlencode("<b>[ALERT] <i>GIVE ME VALID CARD</i></b>");
$maintain = urlencode("<b>[ALERT] <u>GATE ON MAINTENANCE</u>\n~ USE ANOTHER WORKING GATES</b>");
$noregister = urlencode("<b>[ALERT] YOU DON'T REGISTERED YOURSELF. PLEASE REGISTER YOURSELF FIRST TO USE ME\n•• USE /register TO REGISTER ME</b>");
$nocredits = urlencode("<b>️[ALERT] YOU DON'T HAVE SUFFICIENT CREDITS TO USE ME.\n•• RECHARGE NOW BY HITTING /buy</b>");
$buyit = urlencode("<b>Use <code>.credits</code> Know Your Available Credits\n-> 100 CREDITS + PREMIUM ACCESS - 5$\n-> 300 CREDITS + PREMIUM ACCESS - 10$\n-> 500 CREDITS + PREMIUM ACCESS - 15$\n-> 1000 CREDITS + PREMIUM ACCESS - 25$\n>> PING <code>@AHMED</code> For Purchasing\nNote -⟩ We Only Accept Upi And Crytpo</b>");
$nopre = urlencode("<b>YOU NEED TO BE PREMIUM TO USE THIS COMMAND.\nHit /buy to purchase</b>");

// قراءة البيانات
$update = file_get_contents('php://input');
$update = json_decode($update, TRUE);

// متغيرات المستخدم
$cchatid2 = $update["callback_query"]["message"]["chat"]["id"];
$cmessage_id2 = $update["callback_query"]["message"]["message_id"];
$cdata2 = $update["callback_query"]["data"];
$username = $update["message"]["from"]["username"];
$chatId = $update["message"]["chat"]["id"]; 
$chatusername = $update["message"]["chat"]["username"]; 
$chatname = $update["message"]["chat"]["title"]; 
$gId = $update["message"]["from"]["id"];
$userId = $update["message"]["from"]["id"]; 
$firstname = $update["message"]["from"]["first_name"]; 
$message = $update["message"]["text"]; 
$message_id = $update["message"]["message_id"]; 
$r_id = $update["message"]["reply_to_message"];
$r_msg = $update["message"]["reply_to_message"]["text"];
$sender_chat = $update["message"]["sender_chat"]["type"]; 

if($sender_chat == 'channel'){
    exit();
}

if(empty($username)){
    $username = "NoUsername";
}

if(!empty($r_id)){
    $r_msg = $update["message"]["reply_to_message"]["text"]; 
    $message = $message ." ".$r_msg;
}

// ============================================
// CALLBACK HANDLERS
// ============================================

if ($cdata2 == "free"){
    $islive = 'ON';
    $keyboard = ['inline_keyboard' => [[
        ['text' => 'Premium', 'callback_data' => 'paid'], 
        ['text' => 'Buy', 'callback_data' => 'buy'], 
        ['text' => 'Others', 'callback_data' => 'others'], 
        ['text' => 'Finalize', 'callback_data' => 'end']
    ]]];
    
    $freecommands = urlencode("<b>
GATE NAME | COMMANDS
Stripe Auth<code>.ch</code>[<i>$islive</i>]
Stripe Auth<code>.str</code>[<i>$islive</i>]
Mass <code>.mass</code>[<i>$islive</i>]
Razorpay <code>.rp</code>[<i>$islive</i>]
</b>");
    $free = json_encode($keyboard);
    file_get_contents($website."/editMessageText?chat_id=$cchatid2&text=$freecommands&message_id=$cmessage_id2&parse_mode=HTML&reply_markup=$free");
    exit();
}

if ($cdata2 == "paid"){
    $islive = 'ON';
    $keyboard = ['inline_keyboard' => [[
        ['text' => 'Free', 'callback_data' => 'free'], 
        ['text' => 'Others', 'callback_data' => 'others'], 
        ['text' => 'Buy', 'callback_data' => 'buy'], 
        ['text' => 'Finalize', 'callback_data' => 'end']
    ]]];
    
    $freecommands = urlencode("<b>
GATE NAME | COMMANDS
Stripe CHARGE 3$<code>.stc</code>[<i>$islive</i>]
Stripe CHARGE 4$<code>.stp</code>[<i>$islive</i>]
Stripe CHARGE 20$<code>.rape</code>[<i>$islive</i>]
Stripe CHARGE 25$<code>.sto</code>[<i>$islive</i>]
Stripe CHARGE AUTH<code>.sa</code>[<i>$islive</i>]
BRAINTREE <code>.btu</code>[<i>$islive</i>]
SQUARE UP <code>.sq</code>[<i>$islive</i>]
SK Mass <code>.mchk</code>[<i>$islive</i>]
Auth <code>.aut</code>[<i>$islive</i>]
</b>");
    $free = json_encode($keyboard);
    file_get_contents($website."/editMessageText?chat_id=$cchatid2&text=$freecommands&message_id=$cmessage_id2&parse_mode=HTML&reply_markup=$free");
    exit();
}

if ($cdata2 == "others"){
    $keyboard = ['inline_keyboard' => [[
        ['text' => 'FREE', 'callback_data' => 'free'],
        ['text' => 'Buy', 'callback_data' => 'buy'], 
        ['text' => 'Premium','callback_data' => 'paid'],
        ['text' => 'Finalize', 'callback_data' => 'end']
    ]]];
    
    $freecommands = urlencode("<b>->> <code>.credits</code> Know Your Available Credits
->> <code>.info</code> Know Your Information
->> <code>.gen</code> Generate Extrap From Bin
->> <code>.key</code> Check Stripe Key
->> <code>.bin</code> Check Bin
->> <code>.git</code> Check Github Username
->> <code>.weather</code> Check Weather Of Your City
->> <code>.dic</code> Check Word Meaning
->> <code>.tr</code> Translate Given Text
->> <code>.rand</code> Random Identity Generator
->> <code>.http</code> Get Http Proxies
->> <code>.socks4</code> Get Socks4 Proxies
->> <code>.socks5</code> Get Socks5 Proxies

Note-⟩ If you get any type of bugs in this bot please inform AHMED</b>");
    $free = json_encode($keyboard);
    file_get_contents($website."/editMessageText?chat_id=$cchatid2&text=$freecommands&message_id=$cmessage_id2&parse_mode=HTML&reply_markup=$free");
    exit();
}

if ($cdata2 == "buy"){
    $keyboard = ['inline_keyboard' => [[
        ['text' => 'Buy Now', 'url' => 'https://t.me/AHMED'], 
        ['text' => 'Premium', 'callback_data' => 'paid'],
        ['text' => 'Finalize', 'callback_data' => 'end']
    ]]];
    
    $freecommands = urlencode("<b>Use <code>.credits</code> Know Your Available Credits
-> 100 CREDITS + PREMIUM ACCESS - 5$
-> 300 CREDITS + PREMIUM ACCESS - 10$
-> 500 CREDITS + PREMIUM ACCESS - 15$
-> 1000 CREDITS + PREMIUM ACCESS - 25$
Note-⟩ We Only Accept [UPI][GIFT CARDS][CRYTPO]</b>");
    $free = json_encode($keyboard);
    file_get_contents($website."/editMessageText?chat_id=$cchatid2&text=$freecommands&message_id=$cmessage_id2&parse_mode=HTML&reply_markup=$free");
    exit();
}

if($cdata2 == "end"){ 
    $finalize = urlencode("<b>Inline Mode Closed  <a href='tg://user?id=$gId'>$firstname</a></b>"); 
    file_get_contents($website."/editMessageText?chat_id=$cchatid2&text=$finalize&message_id=$cmessage_id2&parse_mode=HTML");
    exit();
}

// ============================================
// HELPER FUNCTIONS
// ============================================

function bot($method, $datas=[]){
    global $botToken;
    $url = "https://api.telegram.org/bot".$botToken."/".$method;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $datas);
    $res = curl_exec($ch);
    if(curl_error($ch)){
        var_dump(curl_error($ch));
    }else{
        return json_decode($res);
    }
}

function sendaction($chatId, $action){
    bot('sendchataction', [
        'chat_id'=>$chatId,
        'action'=>$action
    ]);
}

function reply_to($chatId, $message_id, $keyboard, $message) {
    global $website;
    $url = $website."/sendMessage?chat_id=".$chatId."&text=".$message."&reply_to_message_id=".$message_id."&parse_mode=HTML&reply_markup=".$keyboard;
    return file_get_contents($url);
}

function edit_message($chatId, $message_id, $keyboard, $message) {
    global $website;
    $url = $website."/editMessageText?chat_id=".$chatId."&text=".$message."&message_id=".$message_id."&parse_mode=HTML";
    file_get_contents($url);
}

function deleteM($chatId, $message_id) {
    global $website;
    $url = $website."/deleteMessage?chat_id=".$chatId."&message_id=".$message_id;
    file_get_contents($url);
}

function clean($string) {
    $text = preg_replace("/\r|\n/", " ", $string);
    $str1 = preg_replace('/\s+/', ' ', $text);
    $str = preg_replace("/[^0-9]/", " ", $str1);
    $string = trim($str, " ");
    $lista = preg_replace('/\s+/', ' ', $string);
    return $lista; 
}

function multiexplode($delimiters, $string){
    $one = str_replace($delimiters, $delimiters[0], $string);
    $two = explode($delimiters[0], $one);
    return $two;
}

function getStr($string, $start, $end) {
    $str = explode($start, $string);
    $str = explode($end, $str[1]);  
    return $str[0];
}

function getFlags($code){
    $code = strtoupper($code);
    $flags = [
        'US'=>'🇺🇸', 'GB'=>'🇬🇧', 'CA'=>'🇨🇦', 'AU'=>'🇦🇺', 'DE'=>'🇩🇪',
        'FR'=>'🇫🇷', 'IT'=>'🇮🇹', 'ES'=>'🇪🇸', 'BR'=>'🇧🇷', 'MX'=>'🇲🇽',
        'IN'=>'🇮🇳', 'CN'=>'🇨🇳', 'JP'=>'🇯🇵', 'KR'=>'🇰🇷', 'RU'=>'🇷🇺',
        'IQ'=>'🇮🇶', 'SA'=>'🇸🇦', 'AE'=>'🇦🇪', 'EG'=>'🇪🇬', 'TR'=>'🇹🇷'
    ];
    return isset($flags[$code]) ? $flags[$code] : '🏳';
}

// ============================================
// COMMAND: /START
// ============================================

if (strpos($message, "/start") === 0 or strpos($message, "!start") === 0 or strpos($message, ".start") === 0){
    date_default_timezone_set('Asia/Baghdad');
    $currentTime = date('d-m-Y h:i:s A', time());
    
    $keyboard = ['inline_keyboard' => [[
        ['text' => 'Free', 'callback_data' => 'free'], 
        ['text' => 'Premium', 'callback_data' => 'paid'],
        ['text' => 'Others', 'callback_data' => 'others'],
        ['text' => 'Finalize','callback_data' => 'end']
    ]]];
    
    $encodedKeyboard = json_encode($keyboard);
    sendaction($chatId, 'typing');
    
    bot('sendmessage', [
        'chat_id' => $chatId,
        'reply_to_message_id' => $message_id,
        'text' => "<b>HEY <a href='tg://user?id=$gId'>$firstname</a> 🇮🇶\n\nHit /register to use me\nYour ID: <code>$gId</code>\nCurrent Time (Iraq): $currentTime\n\n✨ Made By AHMED</b>",
        'parse_mode' => 'HTML',
        'reply_markup' => $encodedKeyboard
    ]);
    exit();
}

// ============================================
// COMMAND: /BIN
// ============================================

if(strpos($message, '!bin') === 0 or strpos($message, '/bin') === 0 or strpos($message, '.bin') === 0){
    sendaction($chatId, 'typing');
    $bin = substr($message, 5);
    $bin = clean($bin);
    $bin = substr($bin, 0, 6);
    
    if(empty($bin) || strlen($bin) < 6){
        reply_to($chatId, $message_id, '', "[ALERT] <i>GIVE ME VALID BIN</i>");
        exit();
    }
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'http://bins.su/');
    curl_setopt($ch, CURLOPT_USERAGENT, $_SERVER['HTTP_USER_AGENT']);
    curl_setopt($ch, CURLOPT_POST, 1);
    $headers = [
        'Accept: text/html,application/xhtml+xml,application/xml;q=0.9',
        'Content-Type: application/x-www-form-urlencoded',
        'Host: bins.su',
        'Origin: http://bins.su'
    ];
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
    curl_setopt($ch, CURLOPT_POSTFIELDS, 'action=searchbins&bins='.$bin.'&bank=&country=');
    $result = curl_exec($ch);
    
    $bank = trim(strip_tags(getStr($result, '<td>Bank</td></tr><tr><td>', '</td>')));
    $country = getStr($result, '<td>'.$bank.'</td><td>', '</td>');
    $brand = trim(strip_tags(getStr($result, '<td>'.$country.'</td><td>', '</td>')));
    $level = trim(strip_tags(getStr($result, '<td>'.$brand.'</td><td>', '</td>')));
    $type = trim(strip_tags(getStr($result, '<td>'.$level.'</td><td>', '</td>')));
    $flag = getFlags($country);
    
    if(strpos($result, 'No bins found!')) {
        reply_to($chatId, $message_id, '', "<b>❌ BIN BANNED</b>");
        exit();
    }
    
    $binresult = urlencode("<b>══════ 『 AHMED 』══════
✅ Valid BIN
Bin: <code>$bin</code>
Brand: $brand
Level: $level
Bank: $bank
Country: $country $flag
Type: $type
Checked By @$username</b>");
    
    reply_to($chatId, $message_id, '', $binresult);
    exit();
}

// ============================================
// COMMAND: /GEN
// ============================================

if(strpos($message, '!gen') === 0 or strpos($message, '/gen') === 0 or strpos($message, '.gen') === 0){
    sendaction($chatId, 'typing');
    $sss = reply_to($chatId, $message_id, '', "<b>Generating...</b>");
    $respon = json_decode($sss, TRUE);
    $message_id_1 = $respon['result']['message_id'];
    
    $lista = substr($message, 5);
    $lista = clean($lista);
    $cc = multiexplode([":", "/", " ", "|", ""], $lista)[0];
    $mon = multiexplode([":", "/", " ", "|", ""], $lista)[1];
    $year = multiexplode([":", "/", " ", "|", ""], $lista)[2];
    $cvv = multiexplode([":", "/", " ", "|", ""], $lista)[3];
    $amou = multiexplode([":", "/", " ", "|", ""], $lista)[4];
    
    if(empty($lista)){
        $response = urlencode("<b>VALID INPUT PLEASE\nEx: <code>/gen 407544|x|25|xx</code></b>");
        edit_message($chatId, $message_id_1, '', $response);
        exit();
    }
    
    if($mon > 12){
        $response = urlencode("<b>INVALID MONTH</b>");
        edit_message($chatId, $message_id_1, '', $response);
        exit();
    }
    
    if($year > 2029) {
        $response = urlencode("<b>MAXIMUM YEAR SUPPORTED IS 29</b>");
        edit_message($chatId, $message_id_1, '', $response);
        exit();
    }
    
    if(empty($amou)){
        $amou = '10';
    }
    
    $quantity = $amou;
    $cards = [];
    $cc1 = substr($cc, 0, 1);
    
    for($i = 0; $i < $quantity; $i++){
        $bin = substr($cc, 0, 12);
        $digits = 16 - strlen($bin);
        $ccrem = substr(str_shuffle("0123456789"), 0, $digits);
        
        if($mon == 'xx' or $mon == 'x' or empty($mon)){
            $monthdigit = rand(1, 12);
        } else {
            $monthdigit = $mon;
        }
        
        if(strlen($monthdigit) == 1){
            $monthdigit = "0".$monthdigit;
        }
        
        if($year == 'xxxx' or $year == 'xxx' or $year == 'xx' or $year == 'x' or empty($year)){
            $yeardigit = rand(2025, 2029);
        } else {
            $yeardigit = $year;
        }
        
        if($cvv == 'x' or $cvv == '' or $cvv == 'xx' or $cvv == 'xxx' or empty($cvv)){
            if($cc1 == 3){
                $cvvdigit = rand(1000, 9999);
            } else {
                $cvvdigit = rand(100, 999);
            }
        } else {
            $cvvdigit = $cvv;
        }
        
        $ccgen = $bin.$ccrem;
        $cards[] = $ccgen.'|'.$monthdigit.'|'.$yeardigit.'|'.$cvvdigit;
        $cards[] = "\n";
    }
    
    $card = implode($cards);
    
    if(empty($mon)) $mon = 'x';
    if(empty($year)) $year = 'x';
    if(empty($cvv)) $cvv = 'x';
    
    $respo = urlencode("<b>••• CC GENERATOR
•Format Used: $cc|$mon|$year|$cvv

<code>$card</code>

••• Gen By: @$username
••• Bot By: AHMED</b>");
    
    edit_message($chatId, $message_id_1, '', $respo);
    exit();
}

// ============================================
// COMMAND: /KEY (Stripe Key Checker)
// ============================================

if(strpos($message, '!key') === 0 or strpos($message, '/key') === 0 or strpos($message, '.key') === 0){
    $keyboard = ['inline_keyboard' => [[
        ['text' => 'Features', 'callback_data' => 'paid'], 
        ['text' => 'Buy', 'callback_data' => 'buy']
    ]]];
    $keyboard = json_encode($keyboard);
    
    sendaction($chatId, 'typing');
    $sec = substr($message, 5);
    
    if(empty($sec) || strlen($sec) < 25){
        reply_to($chatId, $message_id, $keyboard, $validauth);
        exit();
    }
    
    $fii = substr($sec, 0, 25);
    $newstring = substr($sec, -10);
    
    $sss = reply_to($chatId, $message_id, $keyboard, "<b>Checking Wait...</b>");
    $respon = json_decode($sss, TRUE);
    $message_id_1 = $respon['result']['message_id'];
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://api.stripe.com/v1/tokens');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, "card[number]=4543218722787334&card[exp_month]=07&card[exp_year]=2026&card[cvc]=780");
    curl_setopt($ch, CURLOPT_USERPWD, $sec.':');
    $headers = ['Content-Type: application/x-www-form-urlencoded'];
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    $result = curl_exec($ch);
    
    if(strpos($result, 'api_key_expired')){
        edit_message($chatId, $message_id_1, $keyboard, "<b>❌ DEAD KEY</b>\n<u>KEY:</u> <code>$sec</code>\n<u>REASON:</u> EXPIRED KEY\n\n<b>Bot By: AHMED</b>");
    } elseif(strpos($result, 'Invalid API Key provided')){
        edit_message($chatId, $message_id_1, $keyboard, "<b>═════════ 『 AHMED 』═════════\n❌ DEAD KEY ❌</b>\n<u>KEY:</u> <code>$sec</code>\n<u>REASON:</u> INVALID KEY\n\n<b>Bot By: AHMED</b>");
    } elseif(strpos($result, 'testmode_charges_only') || strpos($result, 'test_mode_live_card')){
        edit_message($chatId, $message_id_1, $keyboard, "<b>═════════ 『 AHMED 』═════════\n❌ DEAD KEY ❌</b>\n<u>KEY:</u> <code>$sec</code>\n<u>REASON:</u> Testmode Charges Only\n\n<b>Bot By: AHMED</b>");
    } else {
        edit_message($chatId, $message_id_1, $keyboard, "<b>═════════ 『 AHMED 』═════════\n✅LIVE KEY✅</b>\n<u>KEY:</u> <code>${fii}xxxxxxxxxxxxxxxxx${newstring}</code>\n<u>RESPONSE:</u> SK LIVE!!\n\n<b>Bot By: AHMED</b>");
        sleep(10);
        deleteM($chatId, $message_id);
    }
    exit();
}

// إذا لم يتطابق أي أمر
if(!empty($message)){
    // يمكنك إضافة رد افتراضي هنا
}

?>