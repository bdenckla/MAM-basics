%{
/*****************************************************************************
 *
 *	$RCSfile: acc2tre.y,v $
 *	$Date: 2001/11/05 15:31:43 $
 *	$Source: /home/richard/Accents/RCS/acc2tre.y,v $
 *	$Revision: 1.7 $
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
 *  Hebrew verses into binary accentual trees.  This module contains
 *  the YACC grammar for the accents.
 *
 *****************************************************************************
 */

#include "accents.h"

/* 
 * Enable debugging code in YACC/bison. Note that yydebug gets set
 * in accents.c in function main().
 */
#define YYDEBUG 1
typedef union token_and_stack_value_type	YYSTYPE;

/* If nonzero indicates that the current verse contains errors. */
static int are_errors = 0;
static int location_printed = 0;

%}

%token <leaf> LOW_PRECEDENCE

%token <leaf> TILDE SOFPASUQ SILLUQ ATNACH SEGOLTA SHALSHELET ZAQEF
%token <leaf> METHIGAZAQEF ZAQEFGADOL REVIA TIFCHA ZARQA PASHTA YETIV
%token <leaf> TEVIR GERESH GERSHAYIM PAZER PAZERGADOL TELISHAGEDOLA
%token <leaf> LEGARMEH MUNACH MAHPAK MEREKA MEREKAKEFULA DARGA AZLA
%token <leaf> TELISHAQETANNA GALGAL MAYELA

%token <leaf> UNKNOWN_ACCENT

%type <node> file tlg_file pasuq silluq_phrase silluq_clause
%type <node> tifcha_silluq_clause zaqef_silluq_clause
%type <node> segolta_silluq_clause atnach_silluq_clause atnach_phrase
%type <node> atnach_clause tifcha_atnach_clause zaqef_atnach_clause
%type <node> segolta_atnach_clause zaqef_phrase zaqef_clause
%type <node> pashta_zaqef_clause revia_zaqef_clause segolta_phrase
%type <node> segolta_clause zarqa_segolta_clause pashta_segolta_clause
%type <node> revia_segolta_clause tifcha_phrase tifcha_clause
%type <node> tevir_tifcha_clause pashta_tifcha_clause
%type <node> revia_tifcha_clause revia_phrase revia_clause
%type <node> legarmeh_revia_clause geresh_revia_clause
%type <node> big_telisha_revia_clause pazer_revia_clause pashta_phrase
%type <node> pashta_clause legarmeh_pashta_clause geresh_pashta_clause
%type <node> big_telisha_pashta_clause pazer_pashta_clause
%type <node> tevir_phrase tevir_clause legarmeh_tevir_clause
%type <node> geresh_tevir_clause big_telisha_tevir_clause
%type <node> pazer_tevir_clause zarqa_phrase zarqa_clause
%type <node> legarmeh_zarqa_clause geresh_zarqa_clause
%type <node> big_telisha_zarqa_clause pazer_zarqa_clause geresh_phrase
%type <node> geresh_clause legarmeh_geresh_clause big_telisha_phrase
%type <node> big_telisha_clause legarmeh_big_telisha_clause
%type <node> pazer_phrase pazer_clause legarmeh_pazer_clause
%type <node> legarmeh_phrase

%start file

%%

file		: tlg_file
		| { $$ = NULL; }
		;

/*
 * tlg_file
 *
 *   Start symbol = tlg_file.  Defined in such a way as to handle
 *   files with any number of verses (as long as the betacode markers
 *   are correctly formatted).
 *
 */
tlg_file	: tlg_file pasuq
		| pasuq
		;

/*
 * pasuq
 *
 *   A fully cantillated Hebrew verse = pasuq.
 *
 */
pasuq		: error	%prec LOW_PRECEDENCE
			{ if (! location_printed)
			    printf("%s\n", location);
			  accents_warning ("yyparse", 3, location);
			  are_errors += 1;
			  location_printed = 1;
			  free_nodes();
			}
		| TILDE error UNKNOWN_ACCENT SOFPASUQ
			{ if (! location_printed)
			    printf("%s\n", location);
			  accents_warning ("yyparse", 5, location);
			  are_errors += 1;
			  location_printed = 1;
			  free_nodes();
			}
		| TILDE silluq_clause error
			{ if (! location_printed)
			    printf("%s\n", location);
			  accents_warning ("yyparse", 6, location);
			  are_errors += 1;
			  location_printed = 1;
			  free_nodes();
			}
		| TILDE silluq_clause SOFPASUQ
			{ if (are_errors) {
			    /* If accdebug is nonzero, the errors have
			     * been reported by yydebug() already;
			     * also, no need to detail the error here
			     * if we are going to display the tree in
			     * full anyway.
			     */
			    if (! accdebug && ! display_tree && display_all)
			      accents_warning ("yyparse", 7, location);
			    if (! location_printed) {
			      printf("%s\n", location);
			      location_printed = 1;
			    }
			    if (display_tree) {
			      /* 0 is the starting indent level */
			      print_tree($2, 0);
			      goto alldone;
			    }
			  }
			  if (display_all) {
			    if (! location_printed)
			      printf("%s\n", location);
			    if (display_tree)
			      /* 0 is the starting indent level */
			      print_tree($2, 0);
			  }
			alldone:
			  are_errors = 0;
			  location_printed = 0;
			  free_nodes(); 
			}
		;

/* 
 * silluq
 *
 *     Silluq and its combinatory possibilities.
 *
 */
silluq_phrase	: error
			{ /*  for vss. like Gen 32:24 that are missing silluq */
			  yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "silluq_phrase", "ERROR");
			}
		| error SILLUQ
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "silluq_phrase", "ERROR");
			}
		| SILLUQ
			{ $$ = add_leaves(1, "silluq_phrase", $1); }
		| MEREKA SILLUQ
			{ $$ = add_leaves(2, "silluq_phrase", $1, $2); }
  		;

silluq_clause	: silluq_phrase
			{ $$ = $1; }
		| tifcha_silluq_clause
			{ $$ = $1; }
		| zaqef_silluq_clause
			{ $$ = $1; }
		| segolta_silluq_clause
			{ $$ = $1; }
		| atnach_silluq_clause
			{ $$ = $1; }
		;

tifcha_silluq_clause : tifcha_clause silluq_phrase
			{ $$ = make_node("silluq_clause", $1, $2); }
/* Tifcha isn't supposed to be able to repeat. Dunno why I wrote this rule.
 *		| tifcha_clause tifcha_silluq_clause
 *			{ $$ = make_node("silluq_clause", $1, $2); }
 */
		;

zaqef_silluq_clause : zaqef_clause silluq_phrase
			{ $$ = make_node("silluq_clause", $1, $2); }
		| zaqef_clause tifcha_silluq_clause
			{ $$ = make_node("silluq_clause", $1, $2); }
		| zaqef_clause zaqef_silluq_clause
			{ $$ = make_node("silluq_clause", $1, $2); }
		;
/*
 * This production is necessitated by one puny little anomalous
 * verse in the MT - Ezra 7:13, where atnach does not occur, and
 * segolta serves as the main clause divider.  Yeivin, par. 228.
 * The verse doesn't have zaqef either, oddly enough.
 */
segolta_silluq_clause : segolta_clause silluq_phrase
			{ $$ = make_node("silluq_clause", $1, $2); }
		| segolta_clause tifcha_silluq_clause
			{ $$ = make_node("silluq_clause", $1, $2); }
		;

atnach_silluq_clause : atnach_clause silluq_phrase
			{ $$ = make_node("silluq_clause", $1, $2); }
		| atnach_clause tifcha_silluq_clause
			{ $$ = make_node("silluq_clause", $1, $2); }
		| atnach_clause zaqef_silluq_clause
			{ $$ = make_node("silluq_clause", $1, $2); }
/* Atnach clauses can't repeat.  We don't want this rule, therefore.
 *		| atnach_clause atnach_silluq_clause
 *			{ $$ = make_node("silluq_clause", $1, $2); }
 */
		;

/*
 * atnach
 *
 *   Atnach and its combinatory possibilities.
 *
 */
atnach_phrase	: error ATNACH
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "atnach_phrase", "ERROR");
			}
		| ATNACH
			{ $$ = add_leaves(1, "atnach_phrase", $1); }
		| MUNACH ATNACH
			{ $$ = add_leaves(2, "atnach_phrase", $1, $2); }
		| MUNACH MUNACH ATNACH
			{ $$ = add_leaves(3, "atnach_phrase", $1, $2, $3); }
		;

atnach_clause   : atnach_phrase
			{ $$ = $1; }
		| tifcha_atnach_clause
			{ $$ = $1; }
		| zaqef_atnach_clause
			{ $$ = $1; }
		| segolta_atnach_clause
			{ $$ = $1; }
		;

tifcha_atnach_clause : tifcha_clause atnach_phrase
			{ $$ = make_node("atnach_clause", $1, $2); }
/* Tifcha isn't supposed to be able to repeat. Dunno why I wrote this rule.
 *		| tifcha_clause tifcha_atnach_clause
 *			{ $$ = make_node("atnach_clause", $1, $2); }
 */		;

zaqef_atnach_clause : zaqef_clause atnach_phrase
			{ $$ = make_node("atnach_clause", $1, $2); }
		| zaqef_clause tifcha_atnach_clause
			{ $$ = make_node("atnach_clause", $1, $2); }
		| zaqef_clause zaqef_atnach_clause
			{ $$ = make_node("atnach_clause", $1, $2); }
		/*
		 * This is here to catch the missing atnach in Exod
		 * 4:10 in the Leningrad MS.
		 */
		| zaqef_clause tevir_clause MEREKA ATNACH error
			{ yyerrok;
			  are_errors += 1;
			  $$ = make_node("atnach_clause", $1,
			       add_leaves(1, "atnach_phrase", "ERROR"));
			}
		;

segolta_atnach_clause : segolta_clause atnach_phrase
			{ $$ = make_node("atnach_clause", $1, $2); }
		| segolta_clause tifcha_atnach_clause
			{ $$ = make_node("atnach_clause", $1, $2); }
		| segolta_clause zaqef_atnach_clause
			{ $$ = make_node("atnach_clause", $1, $2); }
		;

/*
 * zaqef, zaqef gadol
 *
 *    Revia may precede a zaqef-clause with pashta, if another revia
 *    precedes, it may be converted to pashta.  Yetiv seems only to be
 *    able to substitute for the non-revia-replacing pashta.
 *
 */
zaqef_phrase	: error ZAQEF
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "zaqef_phrase", "ERROR");
			}
		| ZAQEF
			{ $$ = add_leaves(1, "zaqef_phrase", $1); }
		/*
		 * Methiga zaqef looks just like AZLA ZAQEF in the M-C BHS
		 * text, as in the LXX MS, too.
		 */
		| METHIGAZAQEF
			{ $$ = add_leaves(1, "zaqef_phrase", $1); }
		| ZAQEFGADOL
			{ $$ = add_leaves(1, "zaqef_phrase", $1); }
 		/*
		 * See Yeivin on shofar illuy and shofar mekarbel.
		 * These signs often are pointed differently than plain
		 * old munach zaqef and munach+munah zaqef in some MSS,
		 * but here in L they are pointed the same as munachs
		 * before zaqef.
		 */
		| MUNACH ZAQEF
			{ $$ = add_leaves(2, "zaqef_phrase", $1, $2); }
		| MUNACH MUNACH ZAQEF
			{ $$ = add_leaves(3, "zaqef_phrase", $1, $2, $3); }
		;

zaqef_clause	: zaqef_phrase
			{ $$ = $1; }
		| pashta_zaqef_clause
			{ $$ = $1; }
		| revia_zaqef_clause
			{ $$ = $1; }
		;

/* 
 * A bit too powerful here.  Revia and pashta can both divide the
 * zaqef clause, as can multiple revias or pashtas.  Revia, though,
 * cannot follow itself too closely, but is rather turned into
 * pashta.
 */
pashta_zaqef_clause : pashta_clause zaqef_phrase
			{ $$ = make_node("zaqef_clause", $1, $2); }
		| pashta_clause pashta_zaqef_clause
			{ $$ = make_node("zaqef_clause", $1, $2); }
		| pashta_clause revia_zaqef_clause
			{ $$ = make_node("zaqef_clause", $1, $2); }
		;

revia_zaqef_clause : revia_clause zaqef_phrase
			{ $$ = make_node("zaqef_clause", $1, $2); }
		| revia_clause pashta_zaqef_clause
			{ $$ = make_node("zaqef_clause", $1, $2); }
		| revia_clause revia_zaqef_clause
			{ $$ = make_node("zaqef_clause", $1, $2); }
		;

/*
 * segolta
 *
 *     Pashta below = converted revia.  Segolta is like a strong zaqef.
 *
 */
segolta_phrase	: error SEGOLTA
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "segolta_phrase", "ERROR");
			}
		| SEGOLTA
			{ $$ = add_leaves(1, "segolta_phrase", $1); }
		| SHALSHELET
			{ $$ = add_leaves(1, "segolta_phrase", $1); }
		| MUNACH SEGOLTA
			{ $$ = add_leaves(2, "segolta_phrase", $1, $2); }
		| MUNACH MUNACH SEGOLTA
			{ $$ = add_leaves(3, "segolta_phrase", $1, $2, $3); }
		;

segolta_clause	: segolta_phrase
			{ $$ = $1; }
		| zarqa_segolta_clause
			{ $$ = $1; }
		| pashta_segolta_clause
			{ $$ = $1; }
		| revia_segolta_clause
			{ $$ = $1; }
		;

zarqa_segolta_clause : zarqa_clause segolta_phrase
			{ $$ = make_node("segolta_clause", $1, $2); }
		| zarqa_clause zarqa_segolta_clause
			{ $$ = make_node("segolta_clause", $1, $2); }
		/* This is here for Isa 45:1.  See Yeivin, p. 205. */
		| zarqa_clause MUNACH MUNACH error
			{ yyerrok;
			  are_errors += 1;
			  $$ = make_node("segolta_clause", $1, 
			       add_leaves(1, "segolta_phrase", "ERROR"));
			}
		/* This is here 'cause of a BHS error at 2Chr 7:5. */
		| zarqa_clause MUNACH error REVIA
			{ yyerrok;
			  are_errors += 1;
			  $$ = make_node("segolta_clause", $1, 
			       add_leaves(1, "segolta_phrase", "ERROR"));
			}
		;

/* 
 * These are all converted revia -> pashtas; they aren't normal
 * pashtas.  In particular, they consist only of a pashta_phrase or a
 * geresh_pashta_clause.  The grammar is, in other words, too powerful
 * here.
 */
pashta_segolta_clause : pashta_clause segolta_phrase
			{ $$ = make_node("segolta_clause", $1, $2); }
		| pashta_clause zarqa_segolta_clause
			{ $$ = make_node("segolta_clause", $1, $2); }
		| pashta_clause pashta_segolta_clause
			{ $$ = make_node("segolta_clause", $1, $2); }
		| pashta_clause revia_segolta_clause
			{ $$ = make_node("segolta_clause", $1, $2); }
		;

revia_segolta_clause : revia_clause segolta_phrase
			{ $$ = make_node("segolta_clause", $1, $2); }
		| revia_clause zarqa_segolta_clause
			{ $$ = make_node("segolta_clause", $1, $2); }
		| revia_clause pashta_segolta_clause
			{ $$ = make_node("segolta_clause", $1, $2); }
		| revia_clause revia_segolta_clause
			{ $$ = make_node("segolta_clause", $1, $2); }
		;

/*
 * shalshelet
 *
 *    See segolta_phrase above.
 *
 */

/*
 * tifcha
 *
 *    Tifcha and its combinatory possibilities.
 *
 */
tifcha_phrase	: error TIFCHA
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "tifcha_phrase", "ERROR");
			}
		| geresh_clause error TIFCHA
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "tifcha_phrase", "ERROR");
			}
		| TIFCHA
			{ $$ = add_leaves(1, "tifcha_phrase", $1); }
		| MEREKA TIFCHA
			{ $$ = add_leaves(2, "tifcha_phrase", $1, $2); }
		| DARGA MEREKAKEFULA TIFCHA
			{ $$ = add_leaves(3, "tifcha_phrase", $1, $2, $3); }
		/*
		 * In Jer 2:31 mayela takes a tevir before it, showing
		 * that it isn't just a conjunctive, but a variant of
		 * tifcha.  It is different, though, because it can
		 * take azla before it - Dan 4:9,18.
		 */
		| MAYELA
			{ $$ = add_leaves(1, "tifcha_phrase", $1); }
		| MEREKA MAYELA
			{ $$ = add_leaves(2, "tifcha_phrase", $1, $2); }
		| AZLA MAYELA
			{ $$ = add_leaves(2, "tifcha_phrase", $1, $2); }
		;

tifcha_clause	: tifcha_phrase
			{ $$ = $1; }
		| tevir_tifcha_clause
			{ $$ = $1; }
		| pashta_tifcha_clause
			{ $$ = $1; }
		| revia_tifcha_clause
			{ $$ = $1; }
		;

tevir_tifcha_clause : tevir_clause tifcha_phrase
			{ $$ = make_node("tifcha_clause", $1, $2); }
		| tevir_clause tevir_tifcha_clause
			{ $$ = make_node("tifcha_clause", $1, $2); }
		;

/* See above on converted tevir -> pashta. */
pashta_tifcha_clause : pashta_clause tifcha_phrase
			{ $$ = make_node("tifcha_clause", $1, $2); }
		| pashta_clause tevir_tifcha_clause
			{ $$ = make_node("tifcha_clause", $1, $2); }
		| pashta_clause pashta_tifcha_clause
			{ $$ = make_node("tifcha_clause", $1, $2); }
		| pashta_clause revia_tifcha_clause
			{ $$ = make_node("tifcha_clause", $1, $2); }
		;

revia_tifcha_clause : revia_clause tifcha_phrase
			{ $$ = make_node("tifcha_clause", $1, $2); }
		| revia_clause tevir_tifcha_clause
			{ $$ = make_node("tifcha_clause", $1, $2); }
		| revia_clause pashta_tifcha_clause
			{ $$ = make_node("tifcha_clause", $1, $2); }
		| revia_clause revia_tifcha_clause
			{ $$ = make_node("tifcha_clause", $1, $2); }
		;


/*
 * revia
 *
 *    Revia and its combinatory possibilities.
 *
 */
revia_phrase	: error REVIA
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "revia_phrase", "ERROR");
			}
		| REVIA
			{ $$ = add_leaves(1, "revia_phrase", $1); }
		| MUNACH REVIA
			{ $$ = add_leaves(2, "revia_phrase", $1, $2); }
		| DARGA MUNACH REVIA
			{ $$ = add_leaves(3, "revia_phrase", $1, $2, $3); }
		/* 
		 * Yeivin says this combo only occurs in Isa 45:1, but
		 * in fact it occurs in two other passages as well.
		 */
		| MUNACH MUNACH REVIA
			{ $$ = add_leaves(3, "revia_phrase", $1, $2, $3); }
		| MUNACH DARGA MUNACH REVIA
			{ $$ = add_leaves(4, "revia_phrase", $1, $2,
					  $3, $4); }
		;

revia_clause	: revia_phrase
			{ $$ = $1; }
		| legarmeh_revia_clause
			{ $$ = $1; }
		| geresh_revia_clause
			{ $$ = $1; }
		| big_telisha_revia_clause
			{ $$ = $1; }
		| pazer_revia_clause
			{ $$ = $1; }
		;

legarmeh_revia_clause : legarmeh_phrase revia_phrase
			{ $$ = make_node("revia_clause", $1, $2); }
		| legarmeh_phrase legarmeh_revia_clause
			{ $$ = make_node("revia_clause", $1, $2); }
		;

geresh_revia_clause : geresh_clause revia_phrase
			{ $$ = make_node("revia_clause", $1, $2); }
		| geresh_clause legarmeh_revia_clause
			{ $$ = make_node("revia_clause", $1, $2); }
		| geresh_clause geresh_revia_clause
			{ $$ = make_node("revia_clause", $1, $2); }
		;

big_telisha_revia_clause : big_telisha_clause revia_phrase
			{ $$ = make_node("revia_clause", $1, $2); }
		| big_telisha_clause legarmeh_revia_clause
			{ $$ = make_node("revia_clause", $1, $2); }
		| big_telisha_clause geresh_revia_clause
			{ $$ = make_node("revia_clause", $1, $2); }
		| big_telisha_clause big_telisha_revia_clause
			{ $$ = make_node("revia_clause", $1, $2); }
		;

pazer_revia_clause : pazer_clause revia_phrase
			{ $$ = make_node("revia_clause", $1, $2); }
		| pazer_clause legarmeh_revia_clause
			{ $$ = make_node("revia_clause", $1, $2); }
		| pazer_clause geresh_revia_clause
			{ $$ = make_node("revia_clause", $1, $2); }
		| pazer_clause big_telisha_revia_clause
			{ $$ = make_node("revia_clause", $1, $2); }
		| pazer_clause pazer_revia_clause
			{ $$ = make_node("revia_clause", $1, $2); }
		;

/*
 * pashta
 *
 *     Pashta and its combinatory possibilities.
 *
 */
pashta_phrase	: error PASHTA
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "pashta_phrase", "ERROR");
			}
		| error YETIV
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "pashta_phrase", "ERROR");
			}
		/*
		 * Problem: the Michigan-Claremont texts occasionally
		 * mistake mahpak before pashta for yetiv; since
		 * pashta can be repeated, this comes out as a legal
		 * combination.  See Jer 34:3, 37:7, 50:11; Job 3:16.
		 */
		| YETIV
			{ $$ = add_leaves(1, "pashta_phrase", $1); }
		| PASHTA
			{ $$ = add_leaves(1, "pashta_phrase", $1); }
		| MAHPAK PASHTA
			{ $$ = add_leaves(2, "pashta_phrase", $1, $2); }
		/* Not in Yeivin - Judg 15:13. */
		| MAHPAK MAHPAK PASHTA
			{ $$ = add_leaves(2, "pashta_phrase", $1, $2); }
		/* Strange combination.  Not in Yeivin - 1Sam 30:9.
		 * see also Exod 10:13 */
		| MAHPAK MEREKA PASHTA
			{ $$ = add_leaves(2, "pashta_phrase", $1, $2); }
		| MEREKA PASHTA
			{ $$ = add_leaves(2, "pashta_phrase", $1, $2); }
		| AZLA MAHPAK PASHTA
			{ $$ = add_leaves(3, "pashta_phrase", $1, $2, $3); }
		| AZLA MEREKA PASHTA
			{ $$ = add_leaves(3, "pashta_phrase", $1, $2, $3); }
		| MUNACH MAHPAK PASHTA
			{ $$ = add_leaves(3, "pashta_phrase", $1, $2, $3); }
		| MUNACH MEREKA PASHTA
			{ $$ = add_leaves(3, "pashta_phrase", $1, $2, $3); }
		| TELISHAQETANNA AZLA MAHPAK PASHTA
			{ $$ = add_leaves(4, "pashta_phrase", $1, $2, $3,
					  $4); }
		| TELISHAQETANNA AZLA MEREKA PASHTA
			{ $$ = add_leaves(4, "pashta_phrase", $1, $2, $3,
					  $4); }
		| MUNACH TELISHAQETANNA AZLA MAHPAK PASHTA
			{ $$ = add_leaves(5, "pashta_phrase", $1, $2, $3,
					  $4, $5); }
		| MUNACH TELISHAQETANNA AZLA MEREKA PASHTA
			{ $$ = add_leaves(5, "pashta_phrase", $1, $2, $3,
					  $4, $5); }
		| MUNACH MUNACH TELISHAQETANNA AZLA MAHPAK PASHTA
			{ $$ = add_leaves(6, "pashta_phrase", $1, $2, $3,
					  $4, $5, $6); }
		| MUNACH MUNACH TELISHAQETANNA AZLA MEREKA PASHTA
			{ $$ = add_leaves(6, "pashta_phrase", $1, $2, $3,
					  $4, $5, $6); }
		| MUNACH MUNACH MUNACH TELISHAQETANNA AZLA MAHPAK PASHTA
			{ $$ = add_leaves(7, "pashta_phrase", $1, $2, $3,
					  $4, $5, $6, $7); }
		| MUNACH MUNACH MUNACH TELISHAQETANNA AZLA MEREKA PASHTA
			{ $$ = add_leaves(7, "pashta_phrase", $1, $2, $3,
					  $4, $5, $6, $7); }
		/*
		 * Yeivin's scheme is, by and large, good, but it
		 * misses a number of cases where telisha qetanna
		 * precedes pashta, with no intervening accents
		 */
		| TELISHAQETANNA PASHTA
			{ $$ = add_leaves(2, "pashta_phrase", $1, $2); }
		| MUNACH TELISHAQETANNA PASHTA
			{ $$ = add_leaves(3, "pashta_phrase", $1, $2, $3); }
		;

pashta_clause	: pashta_phrase
			{ $$ = $1; }
		| legarmeh_pashta_clause
			{ $$ = $1; }
		| geresh_pashta_clause
			{ $$ = $1; }
		/* problem here:  If azla is mistaken for pashta,
		 * Accents will not pick up the problem if a geresh
		 * comes next and then later on a revia and even-
		 * tually a zaqef.  Rather, it will parse the azla
		 * as a well-formed pashta clause or phrase!  See,
		 * e.g., Ezek 38:4.
		 */
		| big_telisha_pashta_clause
			{ $$ = $1; }
		| pazer_pashta_clause
			{ $$ = $1; }
		;

legarmeh_pashta_clause : legarmeh_phrase pashta_phrase
			{ $$ = make_node("pashta_clause", $1, $2); }
		| legarmeh_phrase legarmeh_pashta_clause
			{ $$ = make_node("pashta_clause", $1, $2); }
		;
/*
 * Yeivin says the order is big_telisha then geresh, then pashta,
 * but that is not right.  Big telisha often follows geresh, but
 * normally by itself, or with just one servus.
 */
geresh_pashta_clause : geresh_clause pashta_phrase
			{ $$ = make_node("pashta_clause", $1, $2); }
		| geresh_clause legarmeh_pashta_clause
			{ $$ = make_node("pashta_clause", $1, $2); }
		| geresh_clause big_telisha_pashta_clause
			{ $$ = make_node("pashta_clause", $1, $2); }
		| geresh_clause geresh_pashta_clause
			{ $$ = make_node("pashta_clause", $1, $2); }
		;

big_telisha_pashta_clause : big_telisha_clause pashta_phrase
			{ $$ = make_node("pashta_clause", $1, $2); }
		| big_telisha_clause legarmeh_pashta_clause
			{ $$ = make_node("pashta_clause", $1, $2); }
		| big_telisha_clause geresh_pashta_clause
			{ $$ = make_node("pashta_clause", $1, $2); }
		| big_telisha_clause big_telisha_pashta_clause
			{ $$ = make_node("pashta_clause", $1, $2); }
		;

pazer_pashta_clause : pazer_clause pashta_phrase
			{ $$ = make_node("pashta_clause", $1, $2); }
		| pazer_clause legarmeh_pashta_clause
			{ $$ = make_node("pashta_clause", $1, $2); }
		| pazer_clause geresh_pashta_clause
			{ $$ = make_node("pashta_clause", $1, $2); }
		| pazer_clause big_telisha_pashta_clause
			{ $$ = make_node("pashta_clause", $1, $2); }
		| pazer_clause pazer_pashta_clause
			{ $$ = make_node("pashta_clause", $1, $2); }
		;

/*
 * tevir
 *
 *     Tevir and its combinatory possibilities.
 *
 */
tevir_phrase	: error TEVIR
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "tevir_phrase", "ERROR");
			}
		| TEVIR
			{ $$ = add_leaves(1, "tevir_phrase", $1); }
		| DARGA TEVIR
			{ $$ = add_leaves(2, "tevir_phrase", $1, $2); }
		| MEREKA TEVIR
			{ $$ = add_leaves(2, "tevir_phrase", $1, $2); }
		| AZLA DARGA TEVIR
			{ $$ = add_leaves(3, "tevir_phrase", $1, $2,
					  $3); }
		| AZLA MEREKA TEVIR
			{ $$ = add_leaves(3, "tevir_phrase", $1, $2,
					  $3); }
		| MUNACH DARGA TEVIR
			{ $$ = add_leaves(3, "tevir_phrase", $1, $2,
					  $3); }
		| MUNACH MEREKA TEVIR
			{ $$ = add_leaves(3, "tevir_phrase", $1, $2,
					  $3); }
		| TELISHAQETANNA AZLA DARGA TEVIR
			{ $$ = add_leaves(4, "tevir_phrase", $1, $2, $3,
					  $4); }
		| TELISHAQETANNA AZLA MEREKA TEVIR
			{ $$ = add_leaves(4, "tevir_phrase", $1, $2, $3,
					  $4); }
		| MUNACH TELISHAQETANNA AZLA DARGA TEVIR
			{ $$ = add_leaves(5, "tevir_phrase", $1, $2, $3,
					  $4, $5); }
		| MUNACH TELISHAQETANNA AZLA MEREKA TEVIR
			{ $$ = add_leaves(5, "tevir_phrase", $1, $2, $3,
					  $4, $5); }
		;

tevir_clause	: tevir_phrase
			{ $$ = $1; }
		| legarmeh_tevir_clause
			{ $$ = $1; }
		| geresh_tevir_clause
			{ $$ = $1; }
		| big_telisha_tevir_clause
			{ $$ = $1; }
		| pazer_tevir_clause
			{ $$ = $1; }
		;

legarmeh_tevir_clause : legarmeh_phrase tevir_phrase
			{ $$ = make_node("tevir_clause", $1, $2); }
		| legarmeh_phrase legarmeh_tevir_clause
			{ $$ = make_node("tevir_clause", $1, $2); }
		;

/*
 * Yeivin says the order is big_telisha then geresh, then pashta,
 * but that is not right.  Big telisha often follows geresh, but
 * normally by itself, or with just one servus.  Gen 13:1.  See also
 * geresh_pashta_clause above.
 */
geresh_tevir_clause : geresh_clause tevir_phrase
			{ $$ = make_node("tevir_clause", $1, $2); }
		| geresh_clause legarmeh_tevir_clause
			{ $$ = make_node("tevir_clause", $1, $2); }
		| geresh_clause geresh_tevir_clause
			{ $$ = make_node("tevir_clause", $1, $2); }
		| geresh_clause big_telisha_tevir_clause
			{ $$ = make_node("tevir_clause", $1, $2); }
		;

big_telisha_tevir_clause : big_telisha_clause tevir_phrase
			{ $$ = make_node("tevir_clause", $1, $2); }
		| big_telisha_clause legarmeh_tevir_clause
			{ $$ = make_node("tevir_clause", $1, $2); }
		| big_telisha_clause geresh_tevir_clause
			{ $$ = make_node("tevir_clause", $1, $2); }
		| big_telisha_clause big_telisha_tevir_clause
			{ $$ = make_node("tevir_clause", $1, $2); }
		;

pazer_tevir_clause : pazer_clause tevir_phrase
			{ $$ = make_node("tevir_clause", $1, $2); }
		| pazer_clause legarmeh_tevir_clause
			{ $$ = make_node("tevir_clause", $1, $2); }
		| pazer_clause geresh_tevir_clause
			{ $$ = make_node("tevir_clause", $1, $2); }
		| pazer_clause big_telisha_tevir_clause
			{ $$ = make_node("tevir_clause", $1, $2); }
		| pazer_clause pazer_tevir_clause
			{ $$ = make_node("tevir_clause", $1, $2); }
		;

/*
 * zarqa
 *
 *    Before segolta (with only one exception - Isa 45:1).  Zarqa is
 *    probably a specially converted pashta, used before segolta.
 *
 */
zarqa_phrase	: error ZARQA
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "zarqa_phrase", "ERROR");
			}
		| ZARQA
			{ $$ = add_leaves(1, "zarqa_phrase", $1); }
		| MUNACH ZARQA
			{ $$ = add_leaves(2, "zarqa_phrase", $1, $2); }
		| MEREKA ZARQA
			{ $$ = add_leaves(2, "zarqa_phrase", $1, $2); }
		/* The first mereka below is rare. */
		| MEREKA MUNACH ZARQA
			{ $$ = add_leaves(3, "zarqa_phrase", $1, $2, $3); }
		| MEREKA MEREKA ZARQA
			{ $$ = add_leaves(3, "zarqa_phrase", $1, $2, $3); }
		| MUNACH MUNACH ZARQA	
			{ $$ = add_leaves(3, "zarqa_phrase", $1, $2, $3); }
		| MUNACH MEREKA ZARQA
			{ $$ = add_leaves(3, "zarqa_phrase", $1, $2, $3); }
		| AZLA MUNACH ZARQA
			{ $$ = add_leaves(3, "zarqa_phrase", $1, $2, $3); }
		| AZLA MEREKA ZARQA
			{ $$ = add_leaves(3, "zarqa_phrase", $1, $2, $3); }
		| TELISHAQETANNA AZLA MUNACH ZARQA	
			{ $$ = add_leaves(4, "zarqa_phrase", $1, $2, $3,
					  $4); }
		| TELISHAQETANNA AZLA MEREKA ZARQA
			{ $$ = add_leaves(4, "zarqa_phrase", $1, $2, $3,
					  $4); }
		| MUNACH TELISHAQETANNA AZLA MUNACH ZARQA
			{ $$ = add_leaves(5, "zarqa_phrase", $1, $2, $3,
					  $4, $5); }
		| MUNACH TELISHAQETANNA AZLA MEREKA ZARQA
			{ $$ = add_leaves(5, "zarqa_phrase", $1, $2, $3,
					  $4, $5); }
		;

zarqa_clause	: zarqa_phrase
			{ $$ = $1; }
		/* not actually attested */
		| legarmeh_zarqa_clause
			{ $$ = $1; }
		| geresh_zarqa_clause
			{ $$ = $1; }
		| big_telisha_zarqa_clause
			{ $$ = $1; }
		| pazer_zarqa_clause
			{ $$ = $1; }
		;

/* not actually attested, but theoretically possible */
legarmeh_zarqa_clause : legarmeh_phrase zarqa_phrase
			{ $$ = make_node("zarqa_clause", $1, $2); }
		| legarmeh_phrase legarmeh_zarqa_clause
			{ $$ = make_node("zarqa_clause", $1, $2); }
		;

/*
 * Yeivin says the order is big_telisha then geresh, then zarqa,
 * but that is not right.  Big telisha once follows geresh before
 * zarqa (Neh 3:15).  This works basically like geresh_pashta clauses
 * (on which, see above).
 */
geresh_zarqa_clause : geresh_clause zarqa_phrase
			{ $$ = make_node("zarqa_clause", $1, $2); }
		| geresh_clause legarmeh_zarqa_clause
			{ $$ = make_node("zarqa_clause", $1, $2); }
		| geresh_clause big_telisha_zarqa_clause
			{ $$ = make_node("zarqa_clause", $1, $2); }
		| geresh_clause geresh_zarqa_clause
			{ $$ = make_node("zarqa_clause", $1, $2); }
		;

big_telisha_zarqa_clause : big_telisha_clause zarqa_phrase
			{ $$ = make_node("zarqa_clause", $1, $2); }
		| big_telisha_clause legarmeh_zarqa_clause
			{ $$ = make_node("zarqa_clause", $1, $2); }
		| big_telisha_clause geresh_zarqa_clause
			{ $$ = make_node("zarqa_clause", $1, $2); }
		| big_telisha_clause big_telisha_zarqa_clause
			{ $$ = make_node("zarqa_clause", $1, $2); }
		;

pazer_zarqa_clause : pazer_clause zarqa_phrase
			{ $$ = make_node("zarqa_clause", $1, $2); }
		| pazer_clause legarmeh_zarqa_clause
			{ $$ = make_node("zarqa_clause", $1, $2); }
		| pazer_clause geresh_zarqa_clause
			{ $$ = make_node("zarqa_clause", $1, $2); }
		| pazer_clause big_telisha_zarqa_clause
			{ $$ = make_node("zarqa_clause", $1, $2); }
		| pazer_clause pazer_zarqa_clause
			{ $$ = make_node("zarqa_clause", $1, $2); }
		;

/*
 * geresh, gershayim.
 *
 *    Geresh, gershayim, and their servi.
 *
 */
geresh_phrase	: error GERESH
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "geresh_phrase", "ERROR");
			}
		| GERSHAYIM
			{ $$ = add_leaves(1, "geresh_phrase", $1); }
		| MUNACH GERSHAYIM
			{ $$ = add_leaves(2, "geresh_phrase", $1, $2); }
		| GERESH
			{ $$ = add_leaves(1, "geresh_phrase", $1); }
		| MUNACH GERESH
			{ $$ = add_leaves(2, "geresh_phrase", $1, $2); }
		/* 
		 * See above on pashta clauses for a discussion of how
		 * mistaking an azla for a pashta might not result in
		 * a bad parse, as, e.g., in Ezek 38:4.
		 */
		| AZLA GERESH
			{ $$ = add_leaves(2, "geresh_phrase", $1, $2); }
		| TELISHAQETANNA AZLA GERESH
			{ $$ = add_leaves(3, "geresh_phrase", $1, $2,
					  $3); }
		| MUNACH TELISHAQETANNA AZLA GERESH
			{ $$ = add_leaves(4, "geresh_phrase", $1, $2, $3,
					  $4); }
		| MUNACH MUNACH TELISHAQETANNA AZLA GERESH
			{ $$ = add_leaves(5, "geresh_phrase", $1, $2, $3,
					  $4, $5); }
		/* Judg 11:17 & abt. 6 other psgs have this many munachs */
		| MUNACH MUNACH MUNACH TELISHAQETANNA AZLA GERESH
			{ $$ = add_leaves(6, "geresh_phrase", $1, $2, $3,
					  $4, $5, $6); }
		;

geresh_clause	: geresh_phrase
			{ $$ = $1; }
		| legarmeh_geresh_clause
			{ $$ = $1; }
		;

legarmeh_geresh_clause : legarmeh_phrase geresh_phrase
			{ $$ = make_node("geresh_clause", $1, $2); }
		| legarmeh_phrase legarmeh_geresh_clause
			{ $$ = make_node("geresh_clause", $1, $2); }
		;

/*
 * telisha gedola
 *
 *    Telisha gedola and its servi.
 *
 */
big_telisha_phrase : error TELISHAGEDOLA
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "big_telisha_phrase", "ERROR");
			}
		| TELISHAGEDOLA
			{ $$ = add_leaves(1, "big_telisha_phrase", $1); }
		| MUNACH TELISHAGEDOLA
			{ $$ = add_leaves(2, "big_telisha_phrase", $1,
					  $2); }
		| MUNACH MUNACH TELISHAGEDOLA
			{ $$ = add_leaves(3, "big_telisha_phrase", $1,
					  $2, $3); }
		| MUNACH MUNACH MUNACH TELISHAGEDOLA
			{ $$ = add_leaves(4, "big_telisha_phrase", $1,
					  $2, $3, $4); }
		| MUNACH MUNACH MUNACH MUNACH TELISHAGEDOLA
			{ $$ = add_leaves(5, "big_telisha_phrase", $1,
					  $2, $3, $4, $5); }
		| MUNACH MUNACH MUNACH MUNACH MUNACH TELISHAGEDOLA
			{ $$ = add_leaves(6, "big_telisha_phrase", $1,
					  $2, $3, $4, $5, $6); }
		;

big_telisha_clause : big_telisha_phrase
			{ $$ = $1; }
		/* not actually attested, but possible */
		| legarmeh_big_telisha_clause
			{ $$ = $1; }
		;

/* not attested, but theoretically possible */
legarmeh_big_telisha_clause : legarmeh_phrase big_telisha_phrase
			{ $$ = make_node("big_telisha_clause", $1, $2); }
		| legarmeh_phrase legarmeh_big_telisha_clause
			{ $$ = make_node("big_telisha_clause", $1, $2); }
		;

/*
 * pazer, pazer gadol
 *
 *    Pazer gadol and its servi.
 *
 */
pazer_phrase	: error PAZER
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "pazer_phrase", "ERROR");
			}
		| PAZER
			{ $$ = add_leaves(1, "pazer_phrase", $1); }
		| MUNACH PAZER
			{ $$ = add_leaves(2, "pazer_phrase", $1, $2); }
		| MUNACH MUNACH PAZER
			{ $$ = add_leaves(3, "pazer_phrase", $1, $2, $3); }
		| MUNACH MUNACH MUNACH PAZER
			{ $$ = add_leaves(4, "pazer_phrase", $1, $2, $3, $4); }
		| MUNACH MUNACH MUNACH MUNACH PAZER
			{ $$ = add_leaves(5, "pazer_phrase", $1, $2, $3,
					  $4, $5); }
		| MUNACH MUNACH MUNACH MUNACH MUNACH PAZER
			{ $$ = add_leaves(6, "pazer_phrase", $1, $2, $3,
					  $4, $5, $6); }
		| MUNACH MUNACH MUNACH MUNACH MUNACH MUNACH PAZER
			{ $$ = add_leaves(7, "pazer_phrase", $1, $2, $3,
					  $4, $5, $6, $7); }
		| MUNACH GALGAL PAZERGADOL
			{ $$ = add_leaves(3, "pazer_phrase", $1, $2, $3); }
		| MUNACH MUNACH GALGAL PAZERGADOL
			{ $$ = add_leaves(4, "pazer_phrase", $1, $2, $3, $4); }
		| MUNACH MUNACH MUNACH GALGAL PAZERGADOL
			{ $$ = add_leaves(5, "pazer_phrase", $1, $2, $3,
					  $4, $5); }
		| MUNACH MUNACH MUNACH MUNACH GALGAL PAZERGADOL
			{ $$ = add_leaves(6, "pazer_phrase", $1, $2, $3,
					  $4, $5, $6); }
		/* Not in Yeivin - Ezek 48:21, Ezra 6:9. */
		| MUNACH MUNACH MUNACH MUNACH MUNACH GALGAL PAZERGADOL
			{ $$ = add_leaves(7, "pazer_phrase", $1, $2, $3,
					  $4, $5, $6, $7); }
		;

pazer_clause	: pazer_phrase
			{ $$ = $1; }
		| legarmeh_pazer_clause
			{ $$ = $1; }
		;

legarmeh_pazer_clause : legarmeh_phrase pazer_phrase
			{ $$ = make_node("pazer_clause", $1, $2); }
		| legarmeh_phrase legarmeh_pazer_clause
			{ $$ = make_node("pazer_clause", $1, $2); }
		;

/*
 * legarmeh
 *
 *    Legarmeh and its servi.
 *
 */
legarmeh_phrase	: error LEGARMEH
			{ yyerrok;
			  are_errors += 1;
			  $$ = add_leaves(1, "legarmeh_phrase", "ERROR");
			}
		| LEGARMEH
			{ $$ = add_leaves(1, "legarmeh_phrase", $1); }
		| MEREKA LEGARMEH
			{ $$ = add_leaves(2, "legarmeh_phrase", $1, $2); }
		/* 3 passages */
		| AZLA MEREKA LEGARMEH
			{ $$ = add_leaves(3, "legarmeh_phrase", $1, $2, $3); }
		| MUNACH MEREKA LEGARMEH
			{ $$ = add_leaves(3, "legarmeh_phrase", $1, $2, $3); }
		/* rarely */
		| MUNACH MUNACH LEGARMEH
			{ $$ = add_leaves(3, "legarmeh_phrase", $1, $2,
					  $3); }
		;

%%

#include "tnk2acc.c"
