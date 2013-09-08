<?php

    function getSequence($n) {
        $ms = array();
        for ($x = 0;$x<$n;$x++) {
            $ms[] = $x;
        }
        $sequence = array();
        while ($ms) {
            $x = rand(0,count($ms)-1);
            $tmp = array_splice($ms,$x,1);
            $sequence[] = $tmp[0];
        }
        return $sequence;
    }
    
    function dupPair($pairs,$n,$ms,$fs) {
        if ($pairs != NULL) {
            for ($x = 0;$x < $n;$x++) {
                $key = $ms[$x] . $fs[$x];
                if (array_key_exists($key,$pairs)) {
                    //echo "Duplicate Pair found.\n";
                    return True;
                }
            }
        }
        return False;
    }
    
    function repeatedPlayers($pairs,$n,$ms,$fs) {
        if ($pairs != NULL) {
            for ($court = 0;$court < $n/4;$court++) {
                $k1 = $pairs[2*$court];
                $k2 = $pairs(2*($court+1));
            }
            for ($x = 0;$x < $n;$x++) {
                $key = $ms[$x] . $fs[$x];
                if (array_key_exists($key,$pairs)) {
                    //echo "Duplicate Pair found.\n";
                    return True;
                }
            }
            
            return False;
        }
        return False;
    }
    
    function Dups($pairs,$n,$ms,$fs) {
        if (dupPair($pairs,$n,$ms,$fs)) {
            return True;
        }
        if (repeatedPlayers($pairs,$n,$ms,$fs)) {
            return True;
        }
        return False;
    }

    function generateSetSequences($courts) {
        $sets = array(1,2,3);
        $n = $courts * 2;
        $pairs = array();
        $set_sequences = array();
        foreach ($sets as $set) {
            do {
                $ms = getSequence($n);
                $fs = getSequence($n);
            } while (Dups($pairs,$n,$ms,$fs));
            for ($x =0;$x<$n;$x++) {
                $key = sprintf("%02d:%02d",$ms[$x],$fs[$x]);
                $pairs[$key] = 1;
            }
            $set_sequences[] = array($ms,$fs);
        }
        return $set_sequences;
    }
    
?>