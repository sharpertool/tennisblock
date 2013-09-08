<?php

    ob_end_clean();
    
    include 'checkLogin.php';
    include '../inc/Schedule.php';
    require_once '../inc/Teams.php';
    include '../inc/errors.inc';
    include '../lib/common.php';
    require('../inc/play_sheet.php');
    
    $schmgr = ScheduleManager::getInstance();
    if (isset($_SESSION['season'])) {
        $schmgr->setSeason($_SESSION['season']);
        $season = $_SESSION['season'];
    }
    
    if (isset($_POST['matchid'])) {
        $matchid =  $_POST['matchid'];
    
        $pdf=new PlaySheet('L','in', 'Letter');
        
        $matches = $schmgr->GetMatchPlayers($matchid);
        
        //Column titles
        $timestamp = $_POST['timestamp'];
        $d = date("F j, o",$timestamp);
        $header="Friday Night Tennis $d";
        //Data loading
        $pdf->SetFont('Arial','',14);
        $pdf->AddPage();
        $pdf->GenerateSheet($header,$matches);
        $pdf->Output();
    }
?>