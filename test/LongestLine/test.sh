######## Compile
echo 'Compile'
gcc -o longest longest_with_tests.c
echo ''
######## Part 1 - readline (5pts: 1 / 1 / 1 / 2; AON)
# test a one character line (1 pt)
echo 'Test 1'
echo 'X' | ./longest
echo ""
# test a zero character line (1 pt)
echo 'Test 2'
echo '' | ./longest
echo ""
# test a reasonably long line (1 pt)
echo 'Test 3'
echo 'This is a reasonably long line' | ./longest
echo ""
# test an empty file (2 pt)
echo 'Test 4'
./longest < /dev/null
echo ''
######## Part 2 - copy (5 pts: 1 / 1 / 1 / 2; AON)
# test long line last in file (1 pt)
echo 'Test 5'
(echo 'short'; echo 'mid' ; echo 'very long') | ./longest
echo ""
# test long line first in file (1 pt)
echo 'Test 6'
(echo 'very long'; echo 'mid' ; echo 'short') | ./longest
echo ""
# test long line in middle of file (1 pt)
echo 'Test 7'
(echo 'short'; echo 'very long' ; echo 'mid') | ./longest
echo ""
# test all line same length - any line output is ok (2 pt)
echo 'Test 8'
(echo 'line 1'; echo 'line 2' ; echo 'line 3') | ./longest
echo ""
