
/**
 * STS API Engine v1.0 - Sprint 2
 *
 * Supported actions:
 * ?action=health
 * ?action=sheets
 * ?action=portfolio
 * ?action=watch
 * ?action=decision
 * ?action=summary
 * ?action=roles
 * ?action=all
 */

const STS_API_VERSION = "1.0-sprint2";

const STS_API_SHEETS = {
  portfolio: "Portfolio",
  watch: "看盤提醒",
  decision: "v4.3_穩定決策",
  summary: "今日摘要",
  roles: "股票角色表"
};

function doGet(e) {
  const action = (e && e.parameter && e.parameter.action) || "health";

  try {
    if (action === "health") {
      return jsonResponse_({
        ok: true,
        version: STS_API_VERSION,
        updated: now_(),
        availableActions: Object.keys(STS_API_SHEETS).concat(["health", "all", "sheets"]),
        message: "STS API Engine Sprint 2 is running."
      });
    }

    if (action === "sheets") {
      return jsonResponse_({
        ok: true,
        version: STS_API_VERSION,
        updated: now_(),
        sheets: getSheetStatus_()
      });
    }

    if (action === "all") {
      const payload = {
        ok: true,
        version: STS_API_VERSION,
        updated: now_(),
        action: "all"
      };
      Object.keys(STS_API_SHEETS).forEach(function(key) {
        payload[key] = readSheetAsObjects_(STS_API_SHEETS[key]);
      });
      return jsonResponse_(payload);
    }

    if (STS_API_SHEETS[action]) {
      return jsonResponse_({
        ok: true,
        version: STS_API_VERSION,
        updated: now_(),
        action: action,
        data: readSheetAsObjects_(STS_API_SHEETS[action])
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

function getSheetStatus_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const names = ss.getSheets().map(function(s) { return s.getName(); });
  const result = {};
  Object.keys(STS_API_SHEETS).forEach(function(key) {
    const name = STS_API_SHEETS[key];
    const sheet = ss.getSheetByName(name);
    result[key] = {
      expectedName: name,
      exists: !!sheet,
      rows: sheet ? sheet.getLastRow() : 0,
      columns: sheet ? sheet.getLastColumn() : 0
    };
  });
  result._allSheetNames = names;
  return result;
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
      columnCount: values && values[0] ? values[0].length : 0,
      headers: values && values[0] ? values[0].map(h => normalizeHeader_(h)) : []
    };
  }

  const headers = values[0].map(h => normalizeHeader_(h));
  const rawHeaders = values[0];
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
    rawHeaders: rawHeaders,
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
    .replace(/%/g, "pct")
    .replace(/[：:]/g, "_")
    .replace(/[，,]/g, "_");
}

function jsonResponse_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function now_() {
  return Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm:ss");
}
