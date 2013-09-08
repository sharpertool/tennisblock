<?php
define('FPDF_FONTPATH','/var/www/tennis/fpdf/font/');
require('/var/www/tennis/fpdf/fpdf.php');

class PlaySheet extends FPDF
{
    // Matches is an array of 3 matches
    // Each array element, is an array of 3-4 courts
    // each court is a pair of teams
    // each team is a pair of players..
    function GenerateSheet($header,$matches)
    {
        $this->SetMargins(0.25,0);
        $this->SetFont('Arial','B',15);
        $this->SetY(0.5);
        $this->Cell(0,0.25,$header,0,1,'C');

        $match = 1;
        $match_height = 0.25;
        foreach ($matches as $courts) {
            $courtnum = 9;
            $courtidx = 0;
            $text = "Match $match";
            $x = 0.25;
            $y = 0.75+(0.4*5+$match_height)*($match-1);
            $this->SetXY($x,$y);
            $this->SetLeftMargin(0.25);
            $this->SetFillColor(0,0xcc,0xff);
            $this->Cell(10.5,$match_height,$text,1,1,'C',1);
            if (count($courts) > 0) {
                $cellWidth = 10.5/count($courts);
            } else {
                $cellWidth = 10.5/3;
            }
            foreach ($courts as $court)  {
                $pa1 = $court['tapa'];
                $pa2 = $court['tapb'];
                $pb1 = $court['tbpa'];
                $pb2 = $court['tbpb'];
                $texta1 = $pa1->firstname . " " . $pa1->lastname;
                $texta2 = $pa2->firstname . " " . $pa2->lastname;
                $textb1 = $pb1->firstname . " " . $pb1->lastname;
                $textb2 = $pb2->firstname . " " . $pb2->lastname;
                $text = $texta1 . "\n" . $texta2 . "\n    versus\n" . $textb1 . "\n" . $textb2;
                $x = 0.25+$cellWidth*$courtidx;
                $y = 1.+(0.4*5+$match_height)*($match-1);
                $this->Rect($x,$y,$cellWidth,0.4*5);
                $this->SetLeftMargin($x);

                $this->SetXY($x,$y);
                $this->SetFillColor(0xff,0xfd,0xd0);
                $court_txt = "Court $courtnum";
                $this->Cell($cellWidth,0.25,$court_txt,1,1,'C',1);

                $this->SetXY($x,$y+.3);
                $this->Cell($cellWidth,0.25,$texta1,0,1,'C',0);
                $this->Cell($cellWidth,0.25,$texta2,0,1,'C',0);
                #$this->SetFillColor(0x99,0xff,0x66);
                $this->Cell($cellWidth,0.15,'vs.','LRTB',1,'C',1);
                $this->Cell($cellWidth,0.25,$textb1,0,1,'C',0);
                $this->Cell($cellWidth,0.25,$textb2,0,1,'C',0);
                #$this->MultiCell(0.4*5,0.4,$text,0);
                $courtnum++;
                $courtidx++;
            }
            $match++;
        }
    }

    //Simple table
    function BasicTable($header,$data)
    {
        //Header
        foreach($header as $col)
            $this->Cell(40,7,$col,1);
        $this->Ln();
        //Data
        foreach($data as $row)
        {
            foreach($row as $col)
                $this->Cell(40,6,$col,1);
            $this->Ln();
        }
    }
    
    //Better table
    function ImprovedTable($header,$data)
    {
        //Column widths
        $w=array(40,35,40,45);
        //Header
        for($i=0;$i<count($header);$i++)
            $this->Cell($w[$i],7,$header[$i],1,0,'C');
        $this->Ln();
        //Data
        foreach($data as $row)
        {
            $this->Cell($w[0],6,$row[0],'LR');
            $this->Cell($w[1],6,$row[1],'LR');
            $this->Cell($w[2],6,number_format($row[2]),'LR',0,'R');
            $this->Cell($w[3],6,number_format($row[3]),'LR',0,'R');
            $this->Ln();
        }
        //Closure line
        $this->Cell(array_sum($w),0,'','T');
    }
    
    //Colored table
    function FancyTable($header,$data)
    {
        //Colors, line width and bold font
        $this->SetFillColor(255,0,0);
        $this->SetTextColor(255);
        $this->SetDrawColor(128,0,0);
        $this->SetLineWidth(.3);
        $this->SetFont('','B');
        //Header
        $w=array(40,35,40,45);
        for($i=0;$i<count($header);$i++)
            $this->Cell($w[$i],7,$header[$i],1,0,'C',true);
        $this->Ln();
        //Color and font restoration
        $this->SetFillColor(224,235,255);
        $this->SetTextColor(0);
        $this->SetFont('');
        //Data
        $fill=false;
        foreach($data as $row)
        {
            $this->Cell($w[0],6,$row[0],'LR',0,'L',$fill);
            $this->Cell($w[1],6,$row[1],'LR',0,'L',$fill);
            $this->Cell($w[2],6,number_format($row[2]),'LR',0,'R',$fill);
            $this->Cell($w[3],6,number_format($row[3]),'LR',0,'R',$fill);
            $this->Ln();
            $fill=!$fill;
        }
        $this->Cell(array_sum($w),0,'','T');
    }
}

?>
