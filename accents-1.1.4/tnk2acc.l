%{
/*****************************************************************************
 *
 *	$RCSfile: tnk2acc.l,v $
 *	$Date: 1997/05/13 13:53:02 $
 *	$Source: /u/richard/Accents/RCS/tnk2acc.l,v $
 *	$Revision: 1.11 $
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
 *  This lexical analyzer file is part of Accents.  It takes input from
 *  stdin (which must represent the text of BHS, as recorded in the
 *  Michigan-Claremont texts), sets the global variable location to the
 *  current passage (e.g. "Gen 1:1"), and tokenizes the input into
 *  individual cantillation signs.  This entire file is #included by
 *  acc2tre.y.
 *
 *  There are a lot of start states below.  But trust me, they cut
 *  down dramatically on the size of the automaton needed to recognize
 *  all the patterns in the text!
 *
 *****************************************************************************
 */

#if STDC_HEADERS
# include <string.h>
#else /* not STDC_HEADERS */
# if HAVE_STRING_H
#  include <string.h>
# else /* not HAVE_STRING_H */
#  include <strings.h>
# endif /* not HAVE_STRING_H */
#endif /* not STDC_HEADERS */

/* Holds current, human-readable bk ch:vs reference. */
char location[BETABUFSIZ];
/* Temporary buffer for human-readable bk ch (new MC) */
char newlocation[BETABUFSIZ];
char *loc_ptr;

/* used here, in acc2tre.y, and in accutil.c (included below) */
int has_legarmeh (char *);

#ifdef yywrap
#undef yywrap
#endif
int yywrap (void);

%}

TEXT			[^ \r\n\-]*

%START			AA BB CC DD EE FF GG HH

%%


<AA>^~			{ BEGIN CC; }
<AA>^[^~].*$		;
<BB>.*$			{ BEGIN DD; }
<DD>^~			{ BEGIN CC; }
^~			{ BEGIN CC; return TILDE; }
<CC>.*$			{
  /* The above pattern is for the *old* CCAT/Michigan-Claremont
   * format, which uses betacode.
   */
			  char *result;
			  /* Convert betacode line to human-readable form */
  			  if ((result = betacode_2_string (yytext)) == NULL)
			    /* it's one of those chapter-initial "t" verse refs */
			    BEGIN BB;
			  else
			    {
			      /* Can't do Psalms, Proverbs, or Job (yet). */
			      if (strncmp (result, "Pss ", 4) == 0 ||
				  strncmp (result, "Psalm", 5) == 0 ||
				  strncmp (result, "Job ", 4) == 0 ||
				  strncmp (result, "Prov ", 5) == 0)
			        {
				  BEGIN AA;
				}
			      else
				BEGIN GG;
			      strncpy (location, result, BETABUFSIZ - 1);
			      location[BETABUFSIZ - 1] = '\0';
			    }
			}

^([1234][ \t]*)?[A-Z][a-z]+[ \t]*$ {
  /* The above pattern is for the *new* CCAT/Michigan-Claremont
   * format, which has booknames at the head of each chapter, and
   * which dispenses with betacode.
   */
			  if (strncmp (yytext, "Psalm", 5) == 0 ||
			      strncmp (yytext, "Job", 3) == 0 ||
			      strncmp (yytext, "Prov", 4) == 0)
			    {
			      BEGIN HH;
			    }
			  else
			    BEGIN EE;
			  strncpy (newlocation, yytext, BETABUFSIZ - 12);
			  newlocation[BETABUFSIZ - 11] = '\0';
			  strcat (newlocation, " ");
			  loc_ptr = newlocation + strlen (newlocation);
			}

<HH>^[^~].*$		;

<EE>^[1-9][0-9]*:/[1-9]	{ BEGIN FF;
			  strcat (newlocation, " ");
			  strncpy (loc_ptr, yytext, 4);
			  loc_ptr[4] = '\0';
			  return TILDE;
			}
<FF>[1-9][0-9]*/[ \t]	{ BEGIN GG;
			  strcpy (location, newlocation);
			  strncat (location, yytext, 4);
			}


<EE,GG>00		{ BEGIN EE;
			  yylval.leaf = "sof pasuq"     ; return SOFPASUQ;  }
<GG>35|75|95/[^ 379\r\n\-?~]*00 {
			  BEGIN EE;
			  yylval.leaf = "silluq"        ; return SILLUQ;
 /* Metheg/silluq (35, 75, 95) plus sof pasuq (00).  Note that some
  * verses are missing silluq in the Leningrad Codex (e.g. Gen 32:24).
  * This occurs quite commonly in some MS types.  The ...3]*... above
  * excludes mayela (73) and other metheg-like strokes.
  */
}
<GG>92			{ yylval.leaf = "atnach"        ; return ATNACH;    }
<GG>(01{TEXT})?01	{ yylval.leaf = "segolta"       ; return SEGOLTA;
 /* Some Tiberian-pointed MSS repeat segolta in the manner of pashta,
  * if a form is penultimately accented.  Just in case, let's allow
  * for such MSS here.
  */
}
<GG>65{TEXT}05		{ yylval.leaf = "shalshelet"    ; return SHALSHELET;}
<GG>63[^01234680]*80	{ yylval.leaf = "methiga-zaqef" ; return METHIGAZAQEF;}
<GG>80			{ yylval.leaf = "zaqef"         ; return ZAQEF;     }
<GG>85			{ yylval.leaf = "zaqefgadol"    ; return ZAQEFGADOL;}
<GG>81			{ yylval.leaf = "revia"         ; return REVIA;     }
<GG>73/(([^ 0123468\r\n\-]|\-[^ 0123468]*)*(\][0-9])?)*(00|92) {
			  yylval.leaf = "mayela"        ; return MAYELA;
 /* Mayela occurs before both atnach and silluq, either on the same
  * word, or else on a preceding word connected by maqqef.  Ga`ya may
  * intervene betwGGn mayela and silluq or atnach, but no other
  * accent.
  */
}
<GG>73			{ yylval.leaf = "tifcha"        ; return TIFCHA;    }
<GG>(82{TEXT})?02	{ yylval.leaf = "zarqa"         ; return ZARQA;
 /* Sometimes zarqa is repeated on the stressed syllable.  Usually
  * it's postpositive, to distinguish it from tsinnorit.  The M-C BHS
  * texts code repeated zarqa as tsinnorit + zarqa (2Sam 3:8, 2Chr
  * 19:2).
  */
}
<GG>(33{TEXT})?03	{ yylval.leaf = "pashta"        ; return PASHTA;    }
<GG>10			{ yylval.leaf = "yetiv"         ; return YETIV;     }
<GG>91			{ yylval.leaf = "tevir"         ; return TEVIR;     }
<GG>61			{ yylval.leaf = "geresh"        ; return GERESH;    }
<GG>62			{ yylval.leaf = "gershayim"     ; return GERSHAYIM; }
<GG>83			{ yylval.leaf = "pazer"         ; return PAZER;     }
<GG>84			{ yylval.leaf = "pazergadol"    ; return PAZERGADOL;}
<GG>14			{ yylval.leaf = "telishagedola" ; return TELISHAGEDOLA;
 /* Ignore 44, i.e. medial telisha gedola, since 14 (prepositive
  * telisha gedola) always precedes it.  This will let us catch a few
  * bizarre cases when geresh (61) occurs on the same word as telisha.
  * Normally the expression would be 14{TEXT}04, and the {TEXT} would
  * swallow up geresh when the two accents occur together.
  */
}
<GG>74{TEXT}05/[^12368]*(\][0-9])?[^12368]*81 {
			  yylval.leaf = "legarmeh"      ; return LEGARMEH;
 /* Only before revia (with some exceptions) does munach+paseq =
  * legarmeh.  Otherwise it's just a conjunctive plus paseq.  We use
  * the right context to detect a subsequent revia.  [^12368] excludes
  * intervening accents like geresh, telisha gedola, etc., but permits
  * intervening munach and darga, as well as additional legarmehs.
  * The next pattern catches legarmehs that don't occur before revia.
  */
}
<GG>74{TEXT}05		{
			  /* There are 17 passages in the MT where a
			   * munach+paseq combination does not precede
			   * revia, but yet still must be counted as
			   * legarmeh.  Has_legarmeh() returns 1 if we
			   * are within such a passage.
			   */
			  if (has_legarmeh (location)) {
			    yylval.leaf = "legarmeh"    ; return LEGARMEH;
			  } else {
			    yylval.leaf = "munach"      ; return MUNACH;
			  }
			}
<GG>74			{ yylval.leaf = "munach"        ; return MUNACH;    }
<GG>70			{ yylval.leaf = "mahpak"        ; return MAHPAK;    }
<GG>71			{ yylval.leaf = "mereka"        ; return MEREKA;    }
<GG>72			{ yylval.leaf = "merekakefula"  ; return MEREKAKEFULA;}
<GG>94			{ yylval.leaf = "darga"         ; return DARGA;     }
<GG>63			{ yylval.leaf = "azla"          ; return AZLA;      }
<GG>24{TEXT}04		{ yylval.leaf = "telishaqetanna"; return TELISHAQETANNA;}
<GG>04|24		{ yylval.leaf = "telishaqetanna"; return TELISHAQETANNA;}
<GG>93			{ yylval.leaf = "galgal"        ; return GALGAL;    }

<GG>35|75|95|44|05|82|52 {
			  /* Scoup up left-over schwa, medial telisha,
			   * paseq, tsinnorit, puncta extraordinaria,
			   * etc.
			   */
			}
<GG>[0-9][0-9]		{ /* Flag anything we don't recognize. */
			   if (accdebug)
			     fprintf(stderr, "Unrecognized accent, %s (%s).\n",
			             yytext, location);
/*			  yylval.leaf = "UNKNOWN ACCENT"; return UNKNOWN_ACCENT; */
			}
<GG>"**"		|
<GG>"*"[^* \r\n\-]+	;
.			|
[\n\r]			;

%%


/*
 * has_legarmeh:
 *
 *   Returns 1 if s points to a passage reference which is one of the
 *   17 places in the MT where munach+paseq precedes an accent other
 *   than revia, but yet is to be interpreted as legarmeh.  Returns
 *   zero otherwise.  See above, 74{TEXT}05.
 */
int
has_legarmeh(char *s)
{

  #define LISTLEN 17

  int i;
  static count = 0;
  /* this old_i stuff assumes the books are in Jewish order */
  static old_i = 0;
  static char *passages[] = { 
    "Gen 28:9",   "Lev 10:6",   "Lev 21:10",
    "1Sam 14:3",  "1Sam 14:47", "2Sam 13:32",
    "2Kgs 18:17", "Isa 36:2",   "Jer 4:19",
    "Jer 38:11",  "Jer 40:11",  "Ezek 9:2",
    "Hag 2:12",   "Ruth 1:2",   "Dan 3:2",
    "Neh 8:7",    "2Chr 26:15"
  };
  
  /* 1Sam 14:47 has two munach+paseq sequences not preceding revia.
   * Only the second occurrence is a legarmeh.  Count starts keeping
   * track of how many munach+paseq sequences we've seen when we get
   * to 1Sam 14:47.
   */
  for (i = old_i; i < LISTLEN; i++)
    {
      if (strcmp(s, passages[i]) == 0)
	/* if i == 4, this is 1Sam 14:47 */
	if ((i != 4) || (++count == 2))
	  {
	    old_i = i;
	    return 1;
	  }
    }
  return 0;

}


/*
 * yywrap:
 *
 *   Standard function called by all good Lex implementations when EOF
 *   is reached.  If it returns 1 (the default), processing stops.  If
 *   it returns 0, processing continues.  It is assumed, if the return
 *   value is 0, that yyin (Lex's input stream) has been redirected to
 *   another open file.  Note that input_files and how_many_input_files
 *   are set up in accents.c (main).
 */
int
yywrap()
{

  static int i = 0;

  if (++i == how_many_input_files)
    return 1;
  else
    {
      yyin = input_files[i];
      return 0;
    }

}
