Create pot file::

    ./bin/i18ndude rebuild-pot --pot devsrc/collective.gmaplocation/src/collective/gmaplocation/locales/gmaplocation.pot --create gmaplocation devsrc/collective.gmaplocation/src/collective/gmaplocation/
    
Sync to po file::

    ./bin/i18ndude sync --pot devsrc/collective.gmaplocation/src/collective/gmaplocation/locales/gmaplocation.pot devsrc/collective.gmaplocation/src/collective/gmaplocation/locales/de/LC_MESSAGES/gmaplocation.po