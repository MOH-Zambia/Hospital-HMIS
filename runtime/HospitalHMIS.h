//////////////////////////////////////////////////////////////////////////
//
// Hospital HMIS - DHIS2 Tools
//
// Copyright (C) 2020, The GRZ Ministry of Health Development Team
// This software is released under the GPLv3 Licence
//
// HospitalHMIS.h - Main application header
//
//////////////////////////////////////////////////////////////////////////

#ifndef HospitalHMIS_H
#define HospitalHMIS_H

// Include the Python header here as it needs to appear before any QT 
// headers anywhere in the app.
#ifdef __MINGW32__
#include <cmath>
#endif
#include <Python.h>

// QT headers
#include <QtGlobal>

#if QT_VERSION >= 0x050000
#include <QtWidgets>
#else
#include <QApplication>
#include <QtGui>
#include <Qt/qurl.h>
#endif

// Application name
const QString PGA_APP_NAME = QString("Hospital HMIS");

// Global function prototypes
int main(int argc, char * argv[]);
bool PingServer(QUrl url);
void delay(int milliseconds);
void cleanup();
unsigned long sdbm(unsigned char *str);
bool shutdownServer(QUrl url);

#endif // HospitalHMIS_H
