#ifndef _MYWIN_
#define _MYWIN_
#include <string>
#include <vector>
#include "gtkmm.h"
#include "dbsqlite3.h"

class MyModelColumns : public Gtk::TreeModel::ColumnRecord
{
public:
  Gtk::TreeModelColumn<Glib::ustring> *col;
  
  MyModelColumns(unsigned ncolumns):col(new Gtk::TreeModelColumn<Glib::ustring>[ncolumns])
  {
    for(unsigned i=0; i<ncolumns; i++)
      add(col[i]);
  }

  ~MyModelColumns()
  {
    delete [] col;
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
  
  Gtk::Label *labels;
  Gtk::Entry *entries;
  dbsqlite3 * con;

  Gtk::TreeView ansicht;
  
  MyModelColumns mcols;
  Glib::RefPtr<Gtk::ListStore> content;
  Gtk::ScrolledWindow scroll;
  
public:
  mywin(const std::vector<std::string> &columns,
	    dbsqlite3 * _con,
	    const std::string &tname);

  ~mywin()
  {
    delete [] labels;
    delete [] entries;
  }

};


#endif
