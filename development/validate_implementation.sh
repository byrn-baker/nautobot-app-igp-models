#!/bin/bash
# Validation script for Nautobot IGP Models implementation
# This script runs comprehensive validation checks

set -e

echo "=================================================="
echo "Nautobot IGP Models - Implementation Validation"
echo "=================================================="
echo ""

FAILED=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

function check_passed() {
    echo -e "${GREEN}✓ $1${NC}"
}

function check_failed() {
    echo -e "${RED}✗ $1${NC}"
    FAILED=1
}

function check_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

echo "Step 1: Code Quality Checks"
echo "----------------------------"

# Check for print statements in production code
echo -n "Checking for debug print() statements... "
if grep -r "print(" nautobot_igp_models/*.py --exclude-dir=tests 2>/dev/null | grep -v "# print(" | grep -v logger > /dev/null; then
    check_failed "Found print() statements in production code"
    grep -r "print(" nautobot_igp_models/*.py --exclude-dir=tests | grep -v "# print(" | grep -v logger
else
    check_passed "No print() statements found"
fi

# Check for TODO/FIXME comments
echo -n "Checking for TODO/FIXME comments... "
TODO_COUNT=$(grep -r "TODO\|FIXME" nautobot_igp_models/*.py 2>/dev/null | wc -l || echo "0")
if [ "$TODO_COUNT" -gt 0 ]; then
    check_warning "Found $TODO_COUNT TODO/FIXME comments"
else
    check_passed "No TODO/FIXME comments"
fi

# Check for Developer Note placeholders in docs
echo -n "Checking for placeholder text in documentation... "
if grep -r "Developer Note" docs/ README.md 2>/dev/null > /dev/null; then
    check_failed "Found 'Developer Note' placeholders in documentation"
    grep -r "Developer Note" docs/ README.md
else
    check_passed "No placeholder text found"
fi

echo ""
echo "Step 2: File Structure Validation"
echo "-----------------------------------"

# Check critical files exist
CRITICAL_FILES=(
    "nautobot_igp_models/models.py"
    "nautobot_igp_models/forms.py"
    "nautobot_igp_models/tables.py"
    "nautobot_igp_models/filters.py"
    "nautobot_igp_models/views.py"
    "nautobot_igp_models/api/serializers.py"
    "nautobot_igp_models/api/views.py"
    "nautobot_igp_models/tests/fixtures.py"
    "nautobot_igp_models/management/commands/load_igp_demo_data.py"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        check_passed "$file exists"
    else
        check_failed "$file is missing"
    fi
done

# Check test files exist
echo -n "Checking test files... "
TEST_COUNT=$(find nautobot_igp_models/tests -name "test_*.py" | wc -l)
if [ "$TEST_COUNT" -ge 10 ]; then
    check_passed "Found $TEST_COUNT test files"
else
    check_failed "Only found $TEST_COUNT test files (expected 10+)"
fi

echo ""
echo "Step 3: Logging Implementation"
echo "-------------------------------"

# Check for logging imports
for file in "nautobot_igp_models/models.py" "nautobot_igp_models/forms.py" "nautobot_igp_models/signals.py"; do
    if [ -f "$file" ]; then
        if grep -q "import logging" "$file" && grep -q "logger = logging.getLogger" "$file"; then
            check_passed "$file has proper logging setup"
        else
            check_failed "$file missing logging setup"
        fi
    fi
done

echo ""
echo "Step 4: Documentation Validation"
echo "----------------------------------"

# Check key documentation files
DOC_FILES=(
    "README.md"
    "docs/user/app_overview.md"
    "docs/user/app_getting_started.md"
    "docs/user/app_use_cases.md"
)

for file in "${DOC_FILES[@]}"; do
    if [ -f "$file" ]; then
        LINES=$(wc -l < "$file")
        if [ "$LINES" -gt 50 ]; then
            check_passed "$file is complete ($LINES lines)"
        else
            check_warning "$file seems short ($LINES lines)"
        fi
    else
        check_failed "$file is missing"
    fi
done

echo ""
echo "Step 5: Model Validation"
echo "-------------------------"

# Check models file for all expected models
MODELS=("IGPRoutingInstance" "ISISConfiguration" "ISISInterfaceConfiguration" "OSPFConfiguration" "OSPFInterfaceConfiguration")

for model in "${MODELS[@]}"; do
    if grep -q "class $model" nautobot_igp_models/models.py; then
        check_passed "Model $model defined"
    else
        check_failed "Model $model not found"
    fi
done

echo ""
echo "Step 6: Test Coverage"
echo "----------------------"

# Count test methods
TEST_METHODS=$(grep -r "def test_" nautobot_igp_models/tests/ | wc -l)
if [ "$TEST_METHODS" -ge 100 ]; then
    check_passed "Found $TEST_METHODS test methods (excellent coverage)"
elif [ "$TEST_METHODS" -ge 50 ]; then
    check_passed "Found $TEST_METHODS test methods (good coverage)"
else
    check_warning "Only found $TEST_METHODS test methods"
fi

echo ""
echo "=================================================="
echo "Validation Summary"
echo "=================================================="

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}"
    echo "✓ ALL VALIDATION CHECKS PASSED!"
    echo ""
    echo "Your implementation is ready for:"
    echo "  • Running invoke tests"
    echo "  • Starting development environment"
    echo "  • Loading demo data"
    echo "  • Creating a pull request"
    echo -e "${NC}"
    exit 0
else
    echo -e "${RED}"
    echo "✗ SOME VALIDATION CHECKS FAILED"
    echo ""
    echo "Please review the errors above and fix them."
    echo -e "${NC}"
    exit 1
fi
