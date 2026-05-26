/*****************************************************************************
 *
 *	$RCSfile: accents.h,v $
 *	$Date: 1995/10/15 16:25:46 $
 *	$Source: /u/richard/Accents/RCS/accents.h,v $
 *	$Revision: 1.5 $
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
 *  General includes, global variables, structure definitions, and
 *  prototypes needed throughout accents files.
 *
 *****************************************************************************
 */

#include <stdio.h>
#if STDC_HEADERS
# include <stdlib.h>
# include <stddef.h>
#else
# include <sys/types.h>
#endif /* STDC_HEADERS */

#define BETABUFSIZ 64
#define INDENT_STRING "  "

/* yydebug gets set in accutil.c function main() */
extern int accdebug, yydebug, display_tree, display_all;
extern FILE **input_files;
extern int how_many_input_files;
extern char location[];

typedef struct treenode	tn;

struct treenode
{
  const char *label;
  tn *left;
  tn *right;
  size_t leaves_buflen;
  char *leaves;
};

union token_and_stack_value_type
{
  char *leaf;
  tn *node;
};

/* prototypes for utility and YACC/bison functions */
extern void yyerror (char *);	/* in accents.c */
extern int yyparse (void), yylex (void);

/* prototypes for accents functions */
extern void accents_error (char *, int, char *);
extern void accents_warning (char *, int, char *);
extern char *betacode_2_string (char *);
extern tn *make_node (char *, tn *, tn *);
extern tn *add_leaves (int, const char *, ...);
extern int print_tree (tn *, int);
extern int free_nodes (void);
