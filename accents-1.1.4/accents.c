/*****************************************************************************
 *
 *	$RCSfile: accents.c,v $
 *	$Date: 2004/04/03 04:31:42 $
 *	$Source: /home/richard/Accents/RCS/accents.c,v $
 *	$Revision: 1.12 $
 *	$Author: richard $
 *
 *****************************************************************************
 *
 *  Copyright (C) 1995, Richard L. Goerwitz
 *
 *  This program is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License as
 *  published by the Free Software Foundation; either version 2 of the
 *  License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *  General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program (see the file COPYING); if not, write to
 *  the Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA
 *  02139, USA.
 *
 *****************************************************************************
 *
 *  Main program file for accents, a utility that displays the accents
 *  of Tiberian-pointed biblical texts as trees (flagging any errors
 *  that occur).  Usage is:
 *
 *    accents [-e] [-p] [-h]
 *
 *  where -e tells Accents only to print when it finds errors, and where
 *  -p tells it to print accentual trees, and not just verse references.
 *  -h prints a brief usage message and version number.
 *
 *  There is also a -d option.  You don't want to use it, though,
 *  unless you have looked over the source code and understand what it
 *  does and why.
 *
 *****************************************************************************
 */

#if STDC_HEADERS
# include <string.h>
#else /* not STDC_HEADERS */
# include <malloc.h>
# if HAVE_GETOPT_H
#  include <getopt.h>
# else /* not HAVE_GETOPT_H */
extern int optind, opterr;
# endif /* not HAVE_GETOPT_H */
# if HAVE_STRING_H
#  include <string.h>
# else /* not HAVE_STRING_H */
#  include <strings.h>
# endif /* not HAVE_STRING_H */
#endif /* not STDC_HEADERS */

#if HAVE_UNISTD_H
# include <unistd.h>
#endif

#include "accents.h"

/* used by accents_error() to map error numbers to error messages */
struct err
{
  int num;
  char *text;
};

/* 
 * global switches
 *
 *   yydebug turns on YACC's debugging facilities.  accdebug turns on
 *   Accents' debugging facilities.  display_tree enables display of
 *   accentual parse trees.  display_all enables display for all
 *   passages - not just ones w/ errors.
 */
int yydebug = 0, accdebug = 0;
int display_tree = 0, display_all = 1;

extern FILE *yyin;
FILE **input_files;
int how_many_input_files;

/* for error messages */ 
static char *progname;

/*
 * main:
 *
 *   See the beginning of this file for news on what the options below
 *   do and how to use them.
 */
int main (int argc, char **argv)
{

  int i;
  char *usage;

  /* save progname for error handler below */
  if ((progname = strrchr (argv[0], '/')) == NULL)
    progname = argv[0];
  else
    progname++;

  if ((usage = malloc (strlen (progname) + 64)) == NULL)
    accents_error ("main", 5, "");
  strcpy (usage, "\nusage:  ");
  strcat (usage, progname);
  strcat (usage, " [-p] [-e] (-h prints this usage message)\n");

  /* tell getopt to be quiet (opterr is in unistd.h) */
  opterr = 0;

 /* Option -d (debug) turns on debugging output.  Option -p (print)
  * turns on tree printing.  Option -e turns on output only for verses
  * that contain errors.  Option -h is for help.  -v gives the version.
  */
  while ((i = getopt(argc, argv, "dpehv")) != EOF) {
    switch (i) {
    case 'd':
      yydebug  = 1;
      accdebug = 1;
    case 'p':
      display_tree = 1;
      break;
    case 'e':
      display_all = 0;
      break;
    case 'h':
      fprintf (stderr, "%s", usage);
    case 'v':
      fprintf (stderr, "Accents, version 1.1.3.\n");
      exit (0);
    case '?':
      accents_error("main", 1, usage);
      break;
    }
  }

  /*
   * If optind = argc, then no file names were supplied on the
   * command line; use stdin.  Otherwise, go through and open
   * every file supplied (when optind = argc, we're done).
   */
  if ((how_many_input_files = argc - optind) == 0)
    {
      how_many_input_files = 1;
      if ((input_files = malloc (sizeof (FILE *))) == NULL)
	accents_error ("main", 5, "");
      input_files[0] = stdin;
    }
  else
    {
      /*
       * Open all the input files supplied on the cmd line & stuff
       * them into the FILE * array, input_files.
       */
      input_files = malloc (sizeof(FILE *) * how_many_input_files);
      if (input_files == NULL)
	accents_error ("main", 5, "");
      for (i = 0; how_many_input_files > i; i++)
        {
          input_files[i] = fopen (argv[optind + i], "r");
          if (input_files[i] == NULL)
            accents_error ("main", 2, argv[optind + i]);
        }
    }
 
  /*
   * Some versions of YACC apparently don't check to see if yyin
   * is set before defaulting to stdin.  This may cause problems.
   * On input_files, see the file-opening code above.
   */
  yyin = input_files[0];
  if ((i = yyparse()) != 0)
    accents_warning ("yyparse", 10, "end-of-file encountered while in an error state");
  exit (i);

}


/*
 * yyerror:
 *
 *   This is the function YACC calls when it encounters parsing
 *   errors.
 */
void
yyerror(char *s)
{
  if (accdebug)
    accents_warning ("yyparse", 10, s);
}


/*
 * accents_error:
 *
 *   Error abort procedure.  First argument is the name of the
 *   function where the error occurred.  Second one is the error
 *   number.  Third argument is the object that caused the error.
 *   Program exits with status errno (arg 2).
 */
void
accents_error (char *funcname, int errno, char *msg)
{

#define ERROR_MESSAGE_COUNT 6

  int i;
  char *err_msg = "unknown error";
  static struct err errs[ERROR_MESSAGE_COUNT] =
    {
      { 1, "command-line syntax error" },
      { 2, "cannot find and/or access file, "},
      { 3, "general parsing error " },
      { 4, "betacode parsing error, " },
      { 5, "memory allocation error" },
      { 10, "" }
    };

  for (i = 0; i < ERROR_MESSAGE_COUNT; i++)
    if (errno == errs[i].num)
      {
	err_msg = errs[i].text;
	break;
      }

  fprintf (stderr, "%s error %d", progname, errno);
  fprintf (stderr, " (%s): ", funcname);
  fprintf (stderr, "%s%s\n", err_msg, msg);

  exit (errno);

}


/*
 * accents_warning:
 *
 *   Error message display utility.  First argument is the name of the
 *   function where the problem occurred.  Second one is the warning
 *   number.  Third argument is the object that caused the problem.
 *   Program does NOT exit (cf. accents_error above).
 */
void
accents_warning (char *funcname, int warnno, char *msg)
{

#define WARNING_MESSAGE_COUNT 7

  int i;
  char *warn_msg = "unknown failure";
  static struct err warnings[WARNING_MESSAGE_COUNT] =
    {
      { 1, "non-fatal command-line syntax error" },
      { 3, "general parsing error " },
      { 4, "betacode parsing error, " },
      { 5, "unknown accent, "},
      { 6, "verse is missing sof pasuq, " },
      { 7, "error encountered in " },
      { 10, "" }
    };

  for (i = 0; i < WARNING_MESSAGE_COUNT; i++)
    if (warnno == warnings[i].num)
      {
	warn_msg = warnings[i].text;
	break;
      }

  fprintf (stderr, "%s warning %d", progname, warnno);
  fprintf (stderr, " (%s): ", funcname);
  fprintf (stderr, "%s%s\n", warn_msg, msg);

}
