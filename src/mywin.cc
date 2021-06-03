#include "mywin.h"

//sieht schöner aus
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

//Konstruktor
mywin::mywin(const std::vector<std::string> &columns,
	     dbsqlite3 * _con,
	     const std::string &tname):
  btok(Gtk::Stock::OK),
  title("Suche in Alben"),
  con(_con),
  mcols(columns.size()),
  content(Gtk::ListStore::create(mcols))
{
  //window
  set_title("sttalben");  
  
  set_border_width(5);
  set_size_request(800, 600);
  
  //grid
  grid.set_hexpand(true);
  
  //label
  grid.attach(title, 0,0, 2,1);
  set_margins(title);
  
  //eingabe
  for(unsigned i=0; i<columns.size(); i++)
    {
      labels[i] = Gtk::Label(columns[i]);
      grid.attach(labels[i], 0, i+1, 1,1);
      set_margins(labels[i]);
      
      entries[i].set_hexpand(true);
      grid.attach(entries[i], 1, i+1, 1,1);
      set_margins(entries[i]);
    }
  
  //ok
  set_margins(btok);
  grid.attach(btok, 0, columns.size()+2, 2,1);
  btok.signal_clicked().connect([this, columns, tname] () {
				  this->content->clear();
				  query_db(this->con,
					   columns,
					   this->entries,
					   this->content.operator->(),
					   tname);
				});
  
  //ausgabe
  for(unsigned i=0; i<columns.size(); i++)
    {
      ansicht.append_column(columns[i], mcols.col[i]);
    }
  
  ansicht.set_model(content);
  scroll.add(ansicht);
  //scroll.set_policy(Gtk::PolicyType::AUTOMATIC, Gtk::PolicyType::AUTOMATIC);
  scroll.set_hexpand();
  scroll.set_vexpand();
  set_margins(scroll);
  
  grid.attach(scroll,0, columns.size()+3, 2,1);

  add(grid);
}


