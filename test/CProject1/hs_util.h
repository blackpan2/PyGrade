/*
 * Home Security System
 * Interface to the utility parsing module.
 */
#ifndef HS_UTIL
#define HS_UTIL 0

/*
 * Read the next line of text into 'buffer'. At most 'max' characters
 * will be read; characters after this limit are silently discarded.
 * A NUL ('\0') character is placed after the last character in buffer,
 * so its size must be at least (max + 1) characters.
 *
 * Returns the number of characters placed in the buffer or EOF if
 * end of file is detected.
 */
extern int read_line(char buffer[], int max) ;

/*
 * Parse the string in 'line' using the CSV format from the problem spec.
 * Assumes 'line' is a proper C string ('\0' terminated).
 *
 * Returns true iff the string is sytactically correct.
 */
extern int parse_line(char line[]) ;

/*
 * Return the reading structure corresponding to the last successfully
 * parsed (syntactically correct*) line.
 */
extern struct reading_t get_last_reading() ;

//extern void print_event(struct evnode_t pevent);
#endif
