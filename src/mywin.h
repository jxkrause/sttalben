#ifndef _MYWIN_
#define _MYWIN_
#include <string>
#include <vector>
#include <gtkmm.h>
#include "dbsqlite3.h"

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
