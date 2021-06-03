#ifndef _MYWIN_
#define _MYWIN_
#include <string>
#include <vector>
#include <gtkmm.h>
#include "dbsqlite3.h"

void set_margins(Gtk::Widget &widget)
{
  unsigned x = 6;
  widget.set_margin_start(x);
  widget.set_margin_end(x);
  widget.set_margin_top(x);
  widget.set_margin_bottom(x);  
}

//bis zu 32 Spalten mit Strings
class MyModelColumns : public Gtk::TreeModel::ColumnRecord
{
public:
  Gtk::TreeModelColumn<Glib::ustring> col[32];
  
  MyModelColumns(unsigned ncolumns)
  {
    for(unsigned i=0; i<ncolumns; i++)
      add(col[i]);
  }
};



/*
  Datenbank abfrage bei sqlite3
*/
void query_db(dbsqlite3 * con,
	      const std::vector<std::string> & columns,
	      const Gtk::Entry *entries,
	      Gtk::ListStore *content,
	      const std::string &tname){

  //collect entries
  std::string xquery = "SELECT * from " + tname + " ";
  std::string konjunktion = "WHERE ";
  for(unsigned i=0; i<columns.size(); i++)
    {
      std::string eingabe = entries[i].get_text();
      if(!eingabe.empty())
	{
	  xquery = xquery + konjunktion + " " + columns[i] + " = '" + eingabe + "' ";
	  konjunktion = "AND ";
	}
    }

  con->query_fill_liststore(xquery, content);
  
}

/*
  Fenster 
*/
class mywin : public Gtk::Window
{
  Gtk::Button btok;
  Gtk::Grid grid;
  Gtk::Label title;
  
  Gtk::Label labels[32];
  Gtk::Entry entries[32];
  dbsqlite3 * con;

  Gtk::TreeView ansicht;
  
  MyModelColumns mcols;
  Glib::RefPtr<Gtk::ListStore> content;
  Gtk::ScrolledWindow scroll;
  
  public:
  mywin(const std::vector<std::string> &columns,
	dbsqlite3 * _con,
	const std::string &tname);
};


#endif
