<?php
    class TeamGen
    {
        private $courts;
        private $pairs;
        private $men_head2head;
        private $women_head2head;
        private $opposites;
        private $men;
        private $women;
        private $seq;
        
        public function __construct($courts,$men,$women)
        {
            $this->courts = $courts;
            $this->men = $men;
            $this->women = $women;
            $this->men_head2head = array();
            $this->women_head2head = array();
            $this->opposites = array();
        }
        
        // Generate a sequence of players for this match
        public function generateSetSequences() {
            $n = $this->courts * 2;
            do {
                $sets = array(1,2,3);
                $this->restart();
                foreach ($sets as $set) {
                    $iterations = 0;
                    do {
                        $ms = $this->getSequence();
                        $fs = $this->getSequence();
                        $iterations++;
                    } while ($iterations < 1000 and !$this->Check($ms,$fs));
                    if ($iterations == 1000) {
                        //print "Break, retry the thing..\n";
                        break;
                    }
                    for ($x =0;$x<$n;$x++) {
                        $key = $this->makeKey($ms[$x],$fs[$x]);
                        $this->pairs[$key] = 1;
                    }
                    $seq = array($ms,$fs);
                    $this->seq[] = $seq;
                    $this->updateHead2Head($seq);
                }
                if (count($this->seq) == 3) {
                    // Apply any special rules..
                    // specifically, if Kenny and Carrie are playing, they need to play
                    // together at least once!!!!
                    if ($this->SpecialRules()) {
                        return $this->seq;
                    }
                }
                
            } while(1);
        }
        
        private function restart() {
            $this->pairs = array();
            $this->seq = array();
            $this->men_head2head = array();
            $this->women_head2head = array();
            $this->opposites = array();
        }
        
        // Check a particular sequence to see if this is valid
        // Applies a few different criteria
        // Does not use history..
        private function Check($ms,$fs) {
            if ($this->CheckPairs($ms,$fs)) {
                return False;
            }
            if (!$this->CheckRepeats($ms,$fs)) {
                return False;
            }
            if (!$this->CheckOpposites($ms,$fs)) {
                return False;
            }
            if (! $this->CheckMatchup($ms,$fs)) {
                return False;
            }
            return True;
        }
        
        // Check the NTRP matchup.. I have it set to insure the uNTRP
        // is < 0.7.
        private function CheckMatchup($ms,$fs) {
            $n = $this->courts*2;
            $ok = True;
            for ($x=0;$x<$n;$x=$x+2) {
                $m1 = $this->men[$ms[$x]];
                $f1 = $this->women[$fs[$x]];
                $m2 = $this->men[$ms[$x+1]];
                $f2 = $this->women[$fs[$x+1]];
                
                $t1 = $m1->uNTRP + $f1->uNTRP;
                $t2 = $m2->uNTRP + $f2->uNTRP;
                
                $diff = abs($t1-$t2);
                
                if ($diff > 0.5) {
                    $ok = False;
                    //echo sprintf("Bad Matchup:%f\n",$diff);
                }
            }
            return $ok;
        }

        // Don't let two teams play together two times.. this one is easy.
        private function CheckPairs($ms,$fs) {
            $n = $this->courts*2;
            if ($this->pairs != NULL) {
                for ($x = 0;$x < $n;$x++) {
                    $key = $this->makeKey($ms[$x],$fs[$x]);
                    if (array_key_exists($key,$this->pairs)) {
                        //echo "Duplicate Pair found.\n";
                        return True;
                    }
                }
            }
            return False;
        }
        
        private function updateHead2Head($seq) {
            $m = $seq[0];
            $f = $seq[1];
            $n = $this->courts;
            for ($x=0;$x<$this->courts;$x++) {
                $m1 = $m[$x*2];
                $m2 = $m[$x*2+1];
                $f1 = $f[$x*2];
                $f2 = $f[$x*2+1];
                
                // Put lowest first in keys..
                if ($m1 < $m2) {
                    $key = $this->makeKey($m1,$m2);
                } else {
                    $key = $this->makeKey($m2,$m1);
                }
                if (array_key_exists($key,$this->men_head2head)) {
                    $this->men_head2head[$key]++;
                } else {
                    $this->men_head2head[$key] = 1;
                }

                // Put lowest first in keys..
                if ($f1 < $f2) {
                    $key = $this->makeKey($f1,$f2);
                } else {
                    $key = $this->makeKey($f2,$f1);
                }
                if (array_key_exists($key,$this->women_head2head)) {
                    $this->women_head2head[$key]++;
                } else {
                    $this->women_head2head[$key] = 1;
                }

                // Track the opposites
                $key = $this->makeKey($m1,$f2);
                if (array_key_exists($key,$this->opposites)) {
                    $this->opposites[$key]++;
                } else {
                    $this->opposites[$key] = 1;
                }
                $key = $this->makeKey($m2,$f1);
                if (array_key_exists($key,$this->opposites)) {
                    $this->opposites[$key]++;
                } else {
                    $this->opposites[$key] = 1;
                }
            }
        }
        
        private function CheckRepeats($ms,$fs) {
            list($rm,$rw) = $this->repeatedPlayers($ms,$fs);
            if ($rm > 0 or $rw > 0) {
                //print "Repeated head-to-head\n";
                return False;
            }
            return True;
        }
        
        // Avoid havig two guys or two girls play together twice..
        // This one might cause the algorithm to spin a while I'm afraid.
        private function repeatedPlayers($m,$f) {
            $n = $this->courts;
            $rpt_men = 0;
            $rpt_women = 0;
            $rpt_cross = 0;
            if ($this->men_head2head != NULL and $this->women_head2head != NULL) {
                for ($x=0;$x<$this->courts;$x++) {
                    $m1 = $m[$x*2];
                    $m2 = $m[$x*2+1];
                    $f1 = $f[$x*2];
                    $f2 = $f[$x*2+1];
                    
                    $key = $this->makeSortedKey($m1,$m2);
                    if (array_key_exists($key,$this->men_head2head)) {
                        $rpt_men++;
                    }
    
                    // Put lowest first in keys..
                    $key = $this->makeSortedKey($f1,$f2);
                    if (array_key_exists($key,$this->women_head2head)) {
                        $rpt_women++;
                    }
                }
            }
            return array($rpt_men,$rpt_women,$rpt_cross);
        }
        
        // See if someone is playing with or opposite someone else too many times..
        private function CheckOpposites($m,$f) {
            $n = $this->courts*2;
            
            $tmp_opposite = array();
            $tmp_with = array();
            for ($x=0;$x<$this->courts;$x++) {
                $m1 = $m[$x*2];
                $m2 = $m[$x*2+1];
                $f1 = $f[$x*2];
                $f2 = $f[$x*2+1];
                
                $key = $this->makeKey($m1,$f2);
                $tmp_opposite[$key] = 1;
                $key = $this->makeKey($m2,$f1);
                $tmp_opposite[$key] = 1;
                
                $this->makeKey($m1,$f1);
                $tmp_with[$key] = 1;
                $this->makeKey($m2,$f2);
                $tmp_with[$key] = 1;
            }
            for ($mn=0;$mn<$n;$mn++) {
                for ($fn=0;$fn<$n;$fn++) {
                    $key = $this->makeKey($mn,$fn);
                    $with = 0;
                    $opposite = 0;
                    if (array_key_exists($key,$this->pairs)) {
                        $with++;
                    }
                    if (array_key_exists($key,$tmp_with)) {
                        $with++;
                    }
                    if (array_key_exists($key,$this->opposites)) {
                        $opposite = $this->opposites[$key];
                    }
                    if (array_key_exists($key,$tmp_opposite)) {
                        $opposite = $opposite + $tmp_opposite[$key];
                    }
                    if ($with > 0) {
                        if ($opposite > 1) {
                            return False;
                        }
                    } else {
                        if ($opposite > 1)
                        return False;
                    }
                }
            }
            return True;
        }
        
        private function SpecialRules() {
            // Kenny & Carrie Rule
            $n = $this->courts *2;
            $rule_enabled = False;
            $kid = -1;
            $cid = -1;
            for ($x=0;$x<$n;$x++) {
                $m = $this->men[$x];
                if ($m->getName() == "Kenny Wong") {
                    $kid = $x;
                }
                $w = $this->women[$x];
                if ($w->getName() == "Carrie Cornils") {
                    $cid = $x;
                }
            }
            if ($kid >= 0 and $cid >= 0) {
                $rule_enabled = True;
            }
            if ($rule_enabled) {
                // See if they play together at all..
                $key = $this->makeKey($kid,$cid);
                if (array_key_exists($key,$this->pairs)) {
                    return True;
                } else {
                    return False; // They do not play together!!!
                }
            } else {
                return True;
            }
        }

        private function makeKey($a,$b) {
            return sprintf("%02d:%02d",$a,$b);
        }

        private function makeSortedKey($a,$b) {
            if ($a < $b) {
                return sprintf("%02d:%02d",$a,$b);
            } else {
                return sprintf("%02d:%02d",$b,$a);
            }
        }

        // Just generate a random sequence of n items..
        private function getSequence() {
            $n = $this->courts*2;
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
        
        // Print out the sequence, for debug.
        public function DisplaySeq() {
            if ($this->seq == NULL) {
                echo "No Sequence to display\n";
                return;
            }
            $sets = array(1,2,3);
            $court_count = $this->courts;
            $courts = array();
            for ($c = 1;$c<=$court_count;$c++) {
                $courts[] = $c;
            }
            foreach ($sets as $set) {
                $seq = $this->seq[$set-1];
                $ms = $seq[0];
                $fs = $seq[1];
                foreach ($courts as $court) {
                    $x = ($court-1)*2;
                    $m1 = $this->men[$ms[$x]];
                    $f1 = $this->women[$fs[$x]];
                    $m2 = $this->men[$ms[$x+1]];
                    $f2 = $this->women[$fs[$x+1]];
                    
                    $ntrp1 = $m1->NTRP + $f1->NTRP;
                    $ntrp2 = $m2->NTRP + $f2->NTRP;

                    $untrp1 = $m1->uNTRP + $f1->uNTRP;
                    $untrp2 = $m2->uNTRP + $f2->uNTRP;
                    
                    $ntrpdiff = abs($ntrp1-$ntrp2);
                    $untrpdiff = abs($untrp1-$untrp2);
                    
                    $s = sprintf("NTRP Diff:%f uNTRP Diff:%f\n",$ntrpdiff,$untrpdiff);
                    $c1 = sprintf("%s %s and %s %s",$m1->firstname,$m1->lastname,$f1->firstname,$f1->lastname);
                    $c2 = sprintf("%s %s and %s %s",$m2->firstname,$m2->lastname,$f2->firstname,$f2->lastname);
                    
                    echo sprintf("%s versus %s\n%s\n",$c1,$c2,$s);
                }
            }
        }
        
        public function ShowStats() {
            if ($this->seq == NULL) {
                echo "No Sequence to display\n";
                return;
            }
            $n = $this->courts *2;
            // Iterate over the men
            for ($x = 0;$x < $n;$x++) {
                for ($y = 0;$y<$n;$y++) {
                    $key = $this->makeSortedKey($x,$y);
                    if (array_key_exists($key,$this->men_head2head)) {
                        printf("%s plays against %s\n",$this->men[$x]->getName(),$this->men[$y]->getName());
                    }
                    //if (array_key_exists($key,$this->opposites)) {
                    //    printf("%s plays opposite %s\n",$this->men[$x]->getName(),$this->women[$y]->getName());
                    //}
                }
            }
            // Iterate over the women
            for ($x = 0;$x < $n;$x++) {
                for ($y = 0;$y<$n;$y++) {
                    $key = $this->makeSortedKey($x,$y);
                    if (array_key_exists($key,$this->women_head2head)) {
                        printf("%s plays against %s\n",$this->women[$x]->getName(),$this->women[$y]->getName());
                    }
                    //$key = $this->makeKey($y,$x);
                    //if (array_key_exists($key,$this->opposites)) {
                    //    printf("%s plays opposite %s\n",$this->women[$x]->getName(),$this->men[$y]->getName());
                    //}
                }
            }
            
            print "\n\nNow show the matchups.\n";
            // Show what girls a guy plays with/against.
            for ($x = 0;$x < $n;$x++) { // or each guy
                for ($y = 0;$y<$n;$y++) { // for each girl
                    $key = $this->makeKey($x,$y); // Guy girl key.
                    if (array_key_exists($key,$this->pairs) and array_key_exists($key,$this->opposites)) {
                        printf("%s plays with and against %s\n",$this->men[$x]->getName(),$this->women[$y]->getName());
                    } else {
                        if (array_key_exists($key,$this->pairs)) {
                            printf("%s plays with %s.\n",$this->men[$x]->getName(),$this->women[$y]->getName());
                        }
                        if (array_key_exists($key,$this->opposites)) {
                            printf("%s plays opposite %s %d times.\n",$this->men[$x]->getName(),$this->women[$y]->getName(),$this->opposites[$key]);
                        }
                    }
                }
            }
        }
    }



?>