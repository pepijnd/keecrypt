#include "keecryptwindow.h"
#include "ui_keecryptwindow.h"

KeecryptWindow::KeecryptWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::KeecryptWindow)
{
    ui->setupUi(this);
}

KeecryptWindow::~KeecryptWindow()
{
    delete ui;
}
