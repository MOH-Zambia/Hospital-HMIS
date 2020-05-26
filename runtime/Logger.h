//////////////////////////////////////////////////////////////////////////
//
// Hospital HMIS - DHIS2 Tools
//
// Copyright (C) 2020, GRZ Ministry of Health
// This software is released under the GNU General Public License v3.0
//
// Logger.h - Logger Utility
//
//////////////////////////////////////////////////////////////////////////

#ifndef LOGGER_H
#define LOGGER_H

#include <QObject>
#include <QFile>

class Logger : public QObject
{
public:
    static Logger* GetLogger();
    static void ReleaseLogger();
    void Log(const QString& sMessage);

private:
    Logger();
    virtual ~Logger();

private:
    static Logger* m_pThis;
    static QString m_sFileName;
    static QFile *m_Logfile;
};

#endif // LOGGER_H
