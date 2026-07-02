
/**
 * STS API Engine v1.0 - Sprint 1
 *
 * Deploy as Google Apps Script Web App.
 *
 * Supported actions:
 *   ?action=health
 *   ?action=portfolio
 *   ?action=summary
 *   ?action=all
 *
 * First deployment:
 *   Deploy -> New deployment -> Web app
 *   Execute as: Me
 *   Who has access: Anyone with the link
 */

const STS_API_VERSION = "1.0-sprint1";

const STS_API_SHEETS = {
  portfolio: "Portfolio",
  summary: "今日摘要"
};

function doGet(e) {
  const action = (e && e.parameter && e.parameter.action) || "health";

  try {
    if (action === "health") {
      return jsonResponse_({
        ok: true,
        version: STS_API_VERSION,
        updated: now_(),
        message: "STS API Engine is running."
      });
    }

    if (action === "portfolio") {
      return jsonResponse_({
        ok: true,
        version: STS_API_VERSION,
        updated: now_(),
        action: "portfolio",
        data: readSheetAsObjects_(STS_API_SHEETS.portfolio)
      });
    }

    if (action === "summary") {
      return jsonResponse_({
        ok: true,
        version: STS_API_VERSION,
        updated: now_(),
        action: "summary",
        data: readSheetAsObjects_(STS_API_SHEETS.summary)
      });
    }

    if (action === "all") {
      return jsonResponse_({
        ok: true,
        version: STS_API_VERSION,
        updated: now_(),
        action: "all",
        portfolio: readSheetAsObjects_(STS_API_SHEETS.portfolio),
        summary: readSheetAsObjects_(STS_API_SHEETS.summary)
      });
    }

    return jsonResponse_({
      ok: false,
      version: STS_API_VERSION,
      updated: now_(),
      error: "Unknown action: " + action
    });

  } catch (err) {
    return jsonResponse_({
      ok: false,
      version: STS_API_VERSION,
      updated: now_(),
      error: String(err),
      stack: err && err.stack ? String(err.stack) : ""
    });
  }
}

function readSheetAsObjects_(sheetName) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);

  if (!sheet) {
    return {
      ok: false,
      sheet: sheetName,
      rows: [],
      error: "Sheet not found: " + sheetName
    };
  }

  const values = sheet.getDataRange().getDisplayValues();

  if (!values || values.length < 2) {
    return {
      ok: true,
      sheet: sheetName,
      rows: [],
      rowCount: 0,
      columnCount: values && values[0] ? values[0].length : 0
    };
  }

  const headers = values[0].map(h => normalizeHeader_(h));
  const rows = [];

  for (let r = 1; r < values.length; r++) {
    const row = {};
    let nonEmpty = false;

    for (let c = 0; c < headers.length; c++) {
      const key = headers[c] || ("col_" + (c + 1));
      const value = values[r][c];
      row[key] = value;
      if (String(value).trim() !== "") nonEmpty = true;
    }

    if (nonEmpty) rows.push(row);
  }

  return {
    ok: true,
    sheet: sheetName,
    rowCount: rows.length,
    columnCount: headers.length,
    headers: headers,
    rows: rows
  };
}

function normalizeHeader_(header) {
  return String(header || "")
    .trim()
    .replace(/\s+/g, "_")
    .replace(/[\/\\]/g, "_")
    .replace(/[()（）]/g, "")
    .replace(/%/g, "pct");
}

function jsonResponse_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function now_() {
  return Utilities.formatDate(
    new Date(),
    Session.getScriptTimeZone(),
    "yyyy-MM-dd HH:mm:ss"
  );
}
