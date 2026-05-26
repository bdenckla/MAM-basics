/*****************************************************************************
 *
 *	$RCSfile: parsebc.c,v $
 *	$Date: 1995/10/15 02:49:32 $
 *	$Source: /home/richard/Accents/RCS/parsebc.c,v $
 *	$Revision: 1.6 $
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
 *  This file is part of Accents, a program that constructs Tiberian
 *  Hebrew verses into binary accentual trees.  This particular file
 *  contains code that converts so-called betacode lines found in
 *  TLG-formatted files (like the Michigan-Claremont ed. of BHS) into
 *  human-readable form.  It has static variables that get incremented
 *  as the file is read sequentially and the main routine below
 *  (betacode_2_string) gets repeatedly called.
 *
 *****************************************************************************
 */

#if STDC_HEADERS
# include <ctype.h>
#else /* not STDC_HEADERS */
/* don't know what else to do :-) */
# include <ctype.h>
#endif /* not STDC_HEADERS */

#if HAVE_UNISTD_H
# include <unistd.h>
#endif

#include "accents.h"

static void parsebc (char *);

/* 
 * Global structure to hold values for betacode fields.
 */
static struct
{
  char a[BETABUFSIZ];
  char b[BETABUFSIZ];
  char c[BETABUFSIZ];
  int x;
  int y;
} whereami;


/*
 * betacode_2_string:
 *
 *   Takes a betacode string and converts it to a human-readable
 *   string, returning a pointer to that string.  Houses the returned
 *   string in static buffer, so don't worry about storage.  Just
 *   remember that each call to betacode_2_string clobbers the old
 *   string, so save it if you plan on using it later.  Returns NULL
 *   if the betacode string cannot be converted to a valid
 *   human-readable string.  This happens, for instance, at the
 *   beginnings of BHS chapters, where x has a "t" value.
 *
 */
char *
betacode_2_string (char *bc)
{

  static char bc_buf[BETABUFSIZ];

  parsebc (bc);

  /* If whereami.x == 0, we have one of those chapter-initial refs
   * that has a "t" for the x field.  Signal this by returning NULL.
   */
  if (whereami.x == 0)
    return NULL;
  else
    {
      sprintf(bc_buf, "%s %d:%d", whereami.c, whereami.x, whereami.y);
      return bc_buf;
    }
}


/*
 * Convenient char pointer-incrementing macro.
 */
#define INCREMENT_CHARPTR { if ((i > BETABUFSIZ) || (*++charptr == '\0')) \
			      accents_error ("parsebc", 4, bc); }

/*
 * parsebc:
 *
 *   Main betacode parser.
 */
static void
parsebc(char *bc)
{

  int i = 0;
  char *charptr;

  charptr = bc;

  if (*charptr == '~')
    INCREMENT_CHARPTR;

  while (*charptr != '\0')
    {
      switch (*charptr)
	{
	case 'a':
	  whereami.x = whereami.y = 1;
	  INCREMENT_CHARPTR;
	  if (*charptr != '"')
	    accents_error ("parsebc", 4, bc);
	  INCREMENT_CHARPTR;
	  for (i = 0; *charptr != '"'; i++)
	    {
	      whereami.a[i] = *charptr;
	      INCREMENT_CHARPTR;
	    }
	  whereami.a[i] = '\0';
	  ++charptr;
	  break;
	case 'b':
	  whereami.x = whereami.y = 1;
	  INCREMENT_CHARPTR;
	  if (*charptr != '"')
	    accents_error ("parsebc", 4, bc);
	  INCREMENT_CHARPTR;
	  for (i = 0; *charptr != '"'; i++)
	    {
	      whereami.b[i] = *charptr;
	      INCREMENT_CHARPTR;
	    }
	  whereami.b[i] = '\0';
	  ++charptr;
	  break;
	case 'c':
	  whereami.x = whereami.y = 1;
	  INCREMENT_CHARPTR;
	  if (*charptr != '"')
	    accents_error ("parsebc", 4, bc);
	  INCREMENT_CHARPTR;
	  for (i = 0; *charptr != '"'; i++)
	    {
	      whereami.c[i] = *charptr;
	      INCREMENT_CHARPTR;
	    }
	  whereami.c[i] = '\0';
	  ++charptr;
	  break;
	case 'x':
	  whereami.x += 1;
	  whereami.y = 1;
	  switch (*++charptr)
	    {
	    case '\0':
	      break;
	    case '"':
	      whereami.x = 0;
	      INCREMENT_CHARPTR;
	      while (*charptr != '"')
		INCREMENT_CHARPTR;
	      charptr++;
	      break;
	    default:
	      if (! isdigit(*charptr))
		accents_error ("parsebc", 4, bc);
	      whereami.x = 0;
	      while ( isdigit(*charptr) )
		{
		  whereami.x = ( (whereami.x * 10) + (*charptr - '0') );
		  ++charptr;
		}
	      break;
	    }
	  break;
	case 'y':
	  whereami.y += 1;
	  if (*++charptr == '\0')
	    break;
	  if (! isdigit(*charptr))
	    accents_error ("parsebc", 4, bc);
	  whereami.y = 0;
	  while ( isdigit(*charptr) )
	    {
	      whereami.y = ( (whereami.y * 10) + (*charptr - '0') );
	      ++charptr;
	    }
	  break;
	default:
	  /* ignore whitespace between fields and at EOL */
	  if (isspace (*charptr))
	    {
	      charptr++;
	      break;
	    }
	  else
	    /* but flag other unknown characters */
	    accents_error ("parsebc", 4, bc);
	}
    }
}
