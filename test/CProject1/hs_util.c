/*
 * Implementation of the utility module functions.
 *
 * Parsing uses the admittedly clumsy regexp package, but this is
 * much less clumsy than doing the parsing by hand.
 */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <regex.h>

#include "hs_config.h"
#include "hs_util.h"

/*
 * NUL byte (to terminate strings)
 */
#define NUL ('\0')

/*
 * Regular expression for legal five field readings and the
 * associated compiled expression structure.
 */
static char five_fields_re[] =
    "^([0-4]),([1-9][0-9]*),([0-2][0-9]:[0-5][0-9]:[0-5][0-9]),([128]),([0-9][0-9]*)$" ;
static regex_t parse_5 ;

/*
 * Regular expression for legal four field readings and the
 * associated compiled expression structure.
 */
static char four_fields_re[] =
    "^([0-4]),([1-9][0-9]*),([0-2][0-9]:[0-5][0-9]:[0-5][0-9]),([39])$" ;
static regex_t parse_4 ;

/*
 * Structure to hold the submatches from the regular expressions above.
 * 0th entry encompasses the whole matched value.
 * i'th entry, i > 0, encompasses the i'th subfield match (up to 5).
 */
#define MAX_MATCHES (6)
static regmatch_t matches[MAX_MATCHES] ;

/*
 * Reading structure holding the last successfully parsed reading line.
 */
static struct reading_t last_reading ;

/*
 * Private module support functions.
 */
static void init_regexps() ;
static int get_int_field(char line[], regmatch_t match) ;
static void get_time_string_field(char to[], char line[], regmatch_t match) ;

/*
 * Read the next line of text into 'buffer'. At most 'max' characters
 * will be read; characters after this limit are silently discarded.
 * A NUL ('\0') character is placed after the last character in buffer,
 * so its size must be at least (max + 1) characters.
 *
 * Returns the number of characters placed in the buffer or EOF if
 * end of file is detected.
 */
int read_line(char buffer[], int max) {
	int next_char ;
	int count = 0 ;

	while( (next_char = getchar()) != '\n' && next_char != EOF ) {
		if( count < max ) {
			buffer[count++] = next_char ;
		}
	}
	buffer[count] = NUL ;

	return (next_char == EOF) ? EOF : count ;
}

/*
 * Parse the string in 'line' using the CSV format from the problem spec.
 * Assumes 'line' is a proper C string ('\0' terminated).
 *
 * Returns true iff the string is sytactically correct.
 */
int parse_line(char line[]) {
	int nmatches = 0 ;	// assume no matches.

	init_regexps() ;

	if( regexec(&parse_5, line, MAX_MATCHES, matches, 0) == 0 ) {
		nmatches = 5 ;
	} else if( regexec(&parse_4, line, MAX_MATCHES, matches, 0) == 0 ) {
		nmatches = 4 ;
	}

	if( nmatches != 0) {
		last_reading.room_id = get_int_field(line, matches[1]) ;
		last_reading.event.sensor = get_int_field(line, matches[2]) ;
		get_time_string_field(last_reading.event.time_stamp,
				line, matches[3]) ;
		last_reading.event.event_id = get_int_field(line, matches[4]) ;
		last_reading.event.event_info =
			(nmatches == 5) ? get_int_field(line, matches[5]) : -1 ;
	}
	return nmatches != 0;
}

/*
 * Return the reading corresponding to the last syntactically correct
 * reading line.
 */
struct reading_t get_last_reading() {
	return last_reading ;
}


/*
 * Local function to do 1 time transform of the string regular expressions
 * into their compiled forms.
 */
static void init_regexps() {
	static int initialized = 0 ;
	int compile_code ;

	if( initialized ) {	// only initialize once.
		return ;
	}
	initialized++ ;

	if( compile_code = regcomp(&parse_5, five_fields_re, REG_EXTENDED) ) {
		printf("Five field regular expression error: %d\n",
			compile_code) ;
		exit(1) ;
	}

	if( compile_code = regcomp(&parse_4, four_fields_re, REG_EXTENDED) ) {
		printf("Four field regular expression error: %d\n",
			compile_code) ;
		exit(1) ;
	}
}

/*
 * Extract regular expression submatch 'field_id' and convert this to an
 * integer. Assumes that (a) there is a 'field_id' submatch and that (b)
 * this is indeed a decimal integer.
 */
#define NUMBER_BASE (10)
static int get_int_field(char line[], regmatch_t match) {
	char *field_start = line + match.rm_so ;

	return (int) strtol(field_start, NULL, NUMBER_BASE) ;
}

/*
 * Extract regular expression submatch 'field_id' from 'line' `and assign it
 * to string 'to'. Assumes that (a) there is a 'field_id' submatch, that
 * (b) this field is in the specified time string format, and (c) the 'to'
 * buffer can hold MAX_TIMESTRING characters plus a terminal NUL.
 */
static void get_time_string_field(char to[], char line[], regmatch_t match) {
	char *field_start = line + match.rm_so ;

	(void)strncpy(to, field_start, MAX_TIMESTRING) ;
	to[MAX_TIMESTRING] = NUL ;
	return ;
}
