#ifndef _MYWIN_
#define _MYWIN_
#include <string>
#include <vector>
#include <gtkmm.h>
#include <sqlite3.h>

//mit Rahmen sind widgets etwas schöner
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
  wird fuer jede Zeil aufgerufen
  erweitert ListStore und fiellt neue Zeile
*/
int CallbackQuery(void *_Pointer, int argc, char **argv, char **columnNames)
{
  Gtk::ListStore *content = (Gtk::ListStore *) _Pointer;
  auto row = *(content->append());
  
  for(int i=1; i<argc; i++)
    {    
      //std::cout << ";" << argv[i];
      gtk_list_store_set(content->gobj(), row.gobj(), i-1, argv[i], -1); 
    }
  //std::cout << std::endl;
  return 0;
  
}

/*
  Datenbank abfrage bei sqlite3
*/
void query_db(sqlite3 * con,
	      const std::vector<std::string> & columns,
	      const Gtk::Entry *entries,
	      Gtk::ListStore *content
	      ){
  char  *err = nullptr;
  
  //collect entries
  std::string xquery = "SELECT * from alben ";
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
  
  //build query
  int ok = sqlite3_exec(con, 
			xquery.c_str(),
			CallbackQuery,
			content,
			&err);
  if(ok != SQLITE_OK)
    {
      std::cout << err << std::endl;
      sqlite3_free(err);
    }
  
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
  sqlite3 * con;

  Gtk::TreeView ansicht;
  
  MyModelColumns mcols;
  Glib::RefPtr<Gtk::ListStore> content;
  Gtk::ScrolledWindow scroll;
  
  public:
  mywin(const std::vector<std::string> &columns,
	sqlite3 * _con):
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
    btok.signal_clicked().connect([this, columns] () {
				    this->content->clear();
				    query_db(this->con, columns, this->entries, this->content.operator->());
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
    //zeigen
    add(grid);
  }
};


#endif
