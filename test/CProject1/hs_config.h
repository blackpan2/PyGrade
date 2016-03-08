/*
 * Home Security System
 * Configuration constants & data types
 */

#ifndef HS_CONFIG
#define HS_CONFIG 0
/*
 * Data structure sizing
 */
#define MAX_TIMESTRING (8)
#define MAX_LINELENGTH (80)

/*
 * Event types
 */
#define T_TEMPERATURE  (1)
#define T_CO           (2)
#define T_INTRUDER     (3)
#define T_TRIM         (8)
#define T_PRINT        (9)

/*
 * Limits for alerts
 */
#define MIN_TEMP  (50)
#define MAX_TEMP  (110)
#define CO_LIMIT  (3000)

/*
 * One sensor event
 * 	The sensor id
 * 	The timestamp
 * 	The event code
 * 	(Optional) event information
 */
struct event_t {
	int sensor ;
	char time_stamp[MAX_TIMESTRING+1];
	int event_id ;
	int event_info ;
} ;

/*
 * A reading consists of a room number, and
 * an event that took place in that room.
 */

struct reading_t {
	int room_id ;
	struct event_t event ;
} ;
#endif
