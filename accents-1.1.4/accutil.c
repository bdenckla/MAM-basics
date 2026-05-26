/*****************************************************************************
 *
 *	$RCSfile: accutil.c,v $
 *	$Date: 1995/10/15 16:26:50 $
 *	$Source: /home/richard/Accents/RCS/accutil.c,v $
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
 *  This file contains utilities for Accents, a program that constructs
 *  Tiberian Hebrew verses into binary accentual trees.  The utilities
 *  contained here include routines for creating binary-tree nodes and for
 *  joining such nodes together into larger trees, a reset routine
 *  (free_nodes), and a binary tree printing routine.
 *
 *****************************************************************************
 */

#if STDC_HEADERS
# include <string.h>
# include <stdarg.h>
#else /* not STDC_HEADERS */
# include <malloc.h>
# include <varargs.h>
# if HAVE_STRING_H
#  include <string.h>
# else /* not HAVE_STRING_H */
#  include <strings.h>
# endif /* not HAVE_STRING_H */
#endif /* not STDC_HEADERS */

#include "accents.h"

/* Structure that holds malloc'd nodes while they're being used. */
struct
{
  int len;
  int allocated;
  tn **array;
} nodes = { 0, 0, NULL };

/* routine that mallocs storage for nodes */
tn *new_node (void);

/*
 * make_node:
 * 
 *   Creates a new tn structure (i.e. a new node in the parse tree),
 *   and makes tree1 its left-hand daughter, and tree2 its right-hand
 *   daughter.
 */
tn *
make_node(char *label, tn *tree1, tn *tree2)
{

  tn *new_tn;

  if (! display_tree)		/* set in accents.c */
    return tree1;
  else
    {
      new_tn = new_node ();
      new_tn->label = label;
      new_tn->left  = tree1;
      new_tn->right = tree2;

      if (accdebug)
	{
	  fprintf(stderr, "made new root node, %s\n", new_tn->label);
	  fprintf(stderr, "daughter nodes are %s and %s\n", new_tn->left->label,
		  new_tn->right->label);
	}
      return new_tn;
    }

}


/*
 * add_leaves:
 *
 *   Routine creates a new tn structure (a tree node), gives it the
 *   label "label" (arg2), and then reads the remaining arguments (all
 *   strings) into the tn struct's leaves field.
 */
tn *
add_leaves(int cnt, const char *label, ...)
{

  size_t i, j;
  char *vptr;
  tn *new_tn;
  va_list ap;

  if (! display_tree)		/* set in accents.c */
    return NULL;
  else
    {
      if (accdebug)
	fprintf(stderr, "collecting leaves into a %s node\n", label);

      new_tn = new_node ();
      new_tn->label = label;
      new_tn->left  = NULL;
      new_tn->right = NULL;

      /* determine how big new_tn->leaves has to be */
#if STDC_HEADERS
      va_start(ap, label);
#else
      va_start(ap);
#endif /* STDC_HEADERS */
      for (i = j = 0; i < cnt; i++)
	j += strlen (va_arg(ap, char *)) + 2;
      va_end(ap);

      /* Be sure new_tn's leaf buffer can hold all the leaves. */
      if (j > new_tn->leaves_buflen)
	{
	  new_tn->leaves_buflen = j;
	  if (new_tn->leaves != NULL)
	    new_tn->leaves = realloc (new_tn->leaves, j);
	  else
	    /* Kludge for systems that don't like realloc (NULL, ...) */
	    new_tn->leaves = malloc (j);
	  if (new_tn->leaves == NULL)
	    accents_error ("add_leaves", 5, "");
	}
      new_tn->leaves[0] = '\0';

      /* tack successive arguments onto new_tn->leaves */
#if STDC_HEADERS
      va_start(ap, label);
#else
      va_start(ap);
#endif /* STDC_HEADERS */
      for (i = 0; i < cnt; ++i)
	{
	  vptr = va_arg(ap, char *);
	  strcat (new_tn->leaves, vptr);
	  strcat (new_tn->leaves, " ");
	}
      va_end(ap);

      if (accdebug)
	{
	  fprintf(stderr, "new node label is: %s\n", new_tn->label);
	  fprintf(stderr, "leaves are: %s\n", new_tn->leaves);
	}

      return new_tn;
    }
}


/*
 * print_tree:
 *
 *   Basically a simple binary tree printing routine.  Note, though,
 *   that the terminal nodes (unlike nonterminals) use their leaves
 *   field.  This is where the names of the leaves for that node are
 *   listed as a single string (see add_leaves() above on how these
 *   are concatenated together.
 */
int
print_tree(tn *tree, int indent_level)
{

  int i;

  if (! display_tree)		/* set in accents.c */
    return 0;
  else
    {
      if (accdebug && ! indent_level)
	fprintf (stderr, "printing_tree\n");
      if (tree != NULL)
	{
	  for (i = 0; i < indent_level; i++)
	    printf (INDENT_STRING);
	  printf ("%d %s\n", indent_level, tree->label);
	  if (tree->left != NULL)
	    {
	      print_tree (tree->left, indent_level + 1);
	      print_tree (tree->right, indent_level + 1);
	    }
	  else
	    {
	      for (i = 0; i <= indent_level; i++)
		printf (INDENT_STRING);
	      printf ("%s\n", tree->leaves);
	    }
	}
      return 1;
    }
}


/*
 * new_node:
 *
 *   Create new node for parse tree, if need be, i.e. malloc and place
 *   the result in nodes.array, then increment nodes.len and
 *   nodes.allocated.  If space has already been allocated, just
 *   re-use an old node, i.e. increment nodes.len and return
 *   nodes.array[nodes.len++].
 */
tn *
new_node (void)
{

  if (nodes.len < nodes.allocated)
    nodes.len++;		/* see return below */
  else
    {
      /* Allocate new tn structure (i.e. a new tree node), increment
       * nodes.len and nodes.allocated, resize nodes.array, and then
       * store the newly allocated node in nodes.array[nodes.len - 1].
       */
      nodes.allocated = ++nodes.len;
      /* Kludge for systems that don't allow realloc (NULL, ...) */
      if (nodes.array != NULL)
	nodes.array = realloc (nodes.array, sizeof (tn *) * nodes.allocated);
      else
	{
	  /* nodes.allocated should be 1 now */
	  nodes.array = malloc (sizeof (tn *) * nodes.allocated);
	  if (accdebug)
	    fprintf(stderr, "initialized nodes.array\n");
	}
      if (nodes.array == NULL)
	accents_error ("new_node", 5, "");
      nodes.array[nodes.len - 1] = malloc (sizeof (tn));
      if (nodes.array[nodes.len - 1] == NULL)
	accents_error ("new_node", 5, "");
      /* start with a one-char buffer (kludge for non-realloc(NULL... systems) */
      nodes.array[nodes.len - 1]->leaves_buflen = 0;
      nodes.array[nodes.len - 1]->leaves = NULL;
      if (accdebug)
	fprintf(stderr, "allocated and stored new node\n");
    }

  return nodes.array[nodes.len - 1];

}


/*
 * free_nodes:
 *
 *   Doesn't really free anything.  Just resets node.len to 0.
 */
int
free_nodes(void)
{

  int old_len;

  if (accdebug)
    fprintf(stderr, "resetting nodes.len (%d) to 0.\n", nodes.len);
  
  old_len = nodes.len;
  nodes.len = 0;
  return old_len;
  
}
