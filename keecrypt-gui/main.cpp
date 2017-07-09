#include "keecryptwindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    KeecryptWindow w;
    w.show();

    return a.exec();
}
