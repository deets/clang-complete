from collections import defaultdict

from ctypes import (
    CDLL,
    c_void_p,
    c_int,
    c_char_p,
    c_ulong,
    c_uint,
    Structure,
    POINTER,
    CFUNCTYPE,
    )

from .util import cfunc

libclang = None

CXIndex = c_void_p
CXClientData = c_void_p

class CXUnsavedFile(Structure):

    _fields_ = [
        ("Filename", c_char_p),
        ("Contents", c_char_p),
        ("Length", c_ulong),
        ]


class CXTranslationUnitImpl(Structure):
    pass

CXTranslationUnit = POINTER(CXTranslationUnitImpl)


class EnumMeta(type):

    def __new__(metacls, name, bases, d):
        lookup = defaultdict(set)
        for name, value in d.iteritems():
            if isinstance(value, int):
                lookup[value].add(name)

        @staticmethod
        def reverse_lookup(value):
            return lookup[value.value]


        d["reverse_lookup"] = reverse_lookup
        return type(name, bases, d)


class CXCursorKind(c_int):
    __metaclass__ = EnumMeta

    CXCursor_UnexposedDecl                 = 1
    CXCursor_StructDecl                    = 2
    CXCursor_UnionDecl                     = 3
    CXCursor_ClassDecl                     = 4
    CXCursor_EnumDecl                      = 5
    CXCursor_FieldDecl                     = 6
    CXCursor_EnumConstantDecl              = 7
    CXCursor_FunctionDecl                  = 8
    CXCursor_VarDecl                       = 9
    CXCursor_ParmDecl                      = 10
    CXCursor_ObjCInterfaceDecl             = 11
    CXCursor_ObjCCategoryDecl              = 12
    CXCursor_ObjCProtocolDecl              = 13
    CXCursor_ObjCPropertyDecl              = 14
    CXCursor_ObjCIvarDecl                  = 15
    CXCursor_ObjCInstanceMethodDecl        = 16
    CXCursor_ObjCClassMethodDecl           = 17
    CXCursor_ObjCImplementationDecl        = 18
    CXCursor_ObjCCategoryImplDecl          = 19
    CXCursor_TypedefDecl                   = 20
    CXCursor_CXXMethod                     = 21
    CXCursor_Namespace                     = 22
    CXCursor_LinkageSpec                   = 23
    CXCursor_Constructor                   = 24
    CXCursor_Destructor                    = 25
    CXCursor_ConversionFunction            = 26
    CXCursor_TemplateTypeParameter         = 27
    CXCursor_NonTypeTemplateParameter      = 28
    CXCursor_TemplateTemplateParameter     = 29
    CXCursor_FunctionTemplate              = 30
    CXCursor_ClassTemplate                 = 31
    CXCursor_ClassTemplatePartialSpecialization = 32
    CXCursor_NamespaceAlias                = 33
    CXCursor_UsingDirective                = 34
    CXCursor_UsingDeclaration              = 35
    CXCursor_TypeAliasDecl                 = 36
    CXCursor_ObjCSynthesizeDecl            = 37
    CXCursor_ObjCDynamicDecl               = 38
    CXCursor_CXXAccessSpecifier            = 39
    CXCursor_FirstDecl                     = CXCursor_UnexposedDecl
    CXCursor_LastDecl                      = CXCursor_CXXAccessSpecifier
    CXCursor_FirstRef                      = 40
    CXCursor_ObjCSuperClassRef             = 40
    CXCursor_ObjCProtocolRef               = 41
    CXCursor_ObjCClassRef                  = 42
    CXCursor_TypeRef                       = 43
    CXCursor_CXXBaseSpecifier              = 44
    CXCursor_TemplateRef                   = 45
    CXCursor_NamespaceRef                  = 46
    CXCursor_MemberRef                     = 47
    CXCursor_LabelRef                      = 48
    CXCursor_OverloadedDeclRef             = 49
    CXCursor_VariableRef                   = 50
    CXCursor_LastRef                       = CXCursor_VariableRef
    CXCursor_FirstInvalid                  = 70
    CXCursor_InvalidFile                   = 70
    CXCursor_NoDeclFound                   = 71
    CXCursor_NotImplemented                = 72
    CXCursor_InvalidCode                   = 73
    CXCursor_LastInvalid                   = CXCursor_InvalidCode
    CXCursor_FirstExpr                     = 100
    CXCursor_UnexposedExpr                 = 100
    CXCursor_DeclRefExpr                   = 101
    CXCursor_MemberRefExpr                 = 102
    CXCursor_CallExpr                      = 103
    CXCursor_ObjCMessageExpr               = 104
    CXCursor_BlockExpr                     = 105
    CXCursor_IntegerLiteral                = 106
    CXCursor_FloatingLiteral               = 107
    CXCursor_ImaginaryLiteral              = 108
    CXCursor_StringLiteral                 = 109
    CXCursor_CharacterLiteral              = 110
    CXCursor_ParenExpr                     = 111
    CXCursor_UnaryOperator                 = 112
    CXCursor_ArraySubscriptExpr            = 113
    CXCursor_BinaryOperator                = 114
    CXCursor_CompoundAssignOperator        = 115
    CXCursor_ConditionalOperator           = 116
    CXCursor_CStyleCastExpr                = 117
    CXCursor_CompoundLiteralExpr           = 118
    CXCursor_InitListExpr                  = 119
    CXCursor_AddrLabelExpr                 = 120
    CXCursor_StmtExpr                      = 121
    CXCursor_GenericSelectionExpr          = 122
    CXCursor_GNUNullExpr                   = 123
    CXCursor_CXXStaticCastExpr             = 124
    CXCursor_CXXDynamicCastExpr            = 125
    CXCursor_CXXReinterpretCastExpr        = 126
    CXCursor_CXXConstCastExpr              = 127
    CXCursor_CXXFunctionalCastExpr         = 128
    CXCursor_CXXTypeidExpr                 = 129
    CXCursor_CXXBoolLiteralExpr            = 130
    CXCursor_CXXNullPtrLiteralExpr         = 131
    CXCursor_CXXThisExpr                   = 132
    CXCursor_CXXThrowExpr                  = 133
    CXCursor_CXXNewExpr                    = 134
    CXCursor_CXXDeleteExpr                 = 135
    CXCursor_UnaryExpr                     = 136
    CXCursor_ObjCStringLiteral             = 137
    CXCursor_ObjCEncodeExpr                = 138
    CXCursor_ObjCSelectorExpr              = 139
    CXCursor_ObjCProtocolExpr              = 140
    CXCursor_ObjCBridgedCastExpr           = 141
    CXCursor_PackExpansionExpr             = 142
    CXCursor_SizeOfPackExpr                = 143
    CXCursor_LambdaExpr                    = 144
    CXCursor_ObjCBoolLiteralExpr           = 145
    CXCursor_ObjCSelfExpr                  = 146
    CXCursor_LastExpr                      = CXCursor_ObjCSelfExpr
    CXCursor_FirstStmt                     = 200
    CXCursor_UnexposedStmt                 = 200
    CXCursor_LabelStmt                     = 201
    CXCursor_CompoundStmt                  = 202
    CXCursor_CaseStmt                      = 203
    CXCursor_DefaultStmt                   = 204
    CXCursor_IfStmt                        = 205
    CXCursor_SwitchStmt                    = 206
    CXCursor_WhileStmt                     = 207
    CXCursor_DoStmt                        = 208
    CXCursor_ForStmt                       = 209
    CXCursor_GotoStmt                      = 210
    CXCursor_IndirectGotoStmt              = 211
    CXCursor_ContinueStmt                  = 212
    CXCursor_BreakStmt                     = 213
    CXCursor_ReturnStmt                    = 214
    CXCursor_GCCAsmStmt                    = 215
    CXCursor_AsmStmt                       = CXCursor_GCCAsmStmt
    CXCursor_ObjCAtTryStmt                 = 216
    CXCursor_ObjCAtCatchStmt               = 217
    CXCursor_ObjCAtFinallyStmt             = 218
    CXCursor_ObjCAtThrowStmt               = 219
    CXCursor_ObjCAtSynchronizedStmt        = 220
    CXCursor_ObjCAutoreleasePoolStmt       = 221
    CXCursor_ObjCForCollectionStmt         = 222
    CXCursor_CXXCatchStmt                  = 223
    CXCursor_CXXTryStmt                    = 224
    CXCursor_CXXForRangeStmt               = 225
    CXCursor_SEHTryStmt                    = 226
    CXCursor_SEHExceptStmt                 = 227
    CXCursor_SEHFinallyStmt                = 228
    CXCursor_MSAsmStmt                     = 229
    CXCursor_NullStmt                      = 230
    CXCursor_DeclStmt                      = 231
    CXCursor_LastStmt                      = CXCursor_DeclStmt
    CXCursor_TranslationUnit               = 300
    CXCursor_FirstAttr                     = 400
    CXCursor_UnexposedAttr                 = 400
    CXCursor_IBActionAttr                  = 401
    CXCursor_IBOutletAttr                  = 402
    CXCursor_IBOutletCollectionAttr        = 403
    CXCursor_CXXFinalAttr                  = 404
    CXCursor_CXXOverrideAttr               = 405
    CXCursor_AnnotateAttr                  = 406
    CXCursor_AsmLabelAttr                  = 407
    CXCursor_LastAttr                      = CXCursor_AsmLabelAttr
    CXCursor_PreprocessingDirective        = 500
    CXCursor_MacroDefinition               = 501
    CXCursor_MacroExpansion                = 502
    CXCursor_MacroInstantiation            = CXCursor_MacroExpansion
    CXCursor_InclusionDirective            = 503
    CXCursor_FirstPreprocessing            = CXCursor_PreprocessingDirective
    CXCursor_LastPreprocessing             = CXCursor_InclusionDirective
    CXCursor_ModuleImportDecl              = 600
    CXCursor_FirstExtraDecl                = CXCursor_ModuleImportDecl
    CXCursor_LastExtraDecl                 = CXCursor_ModuleImportDecl


class CXCursor(Structure):
    _fields_ = [
        ("kind", CXCursorKind),
        ("xdata", c_int),
        ("data", c_void_p * 3),
        ]

    def __repr__(self):
        kind = CXCursorKind.reverse_lookup(self.kind)
        return "<%s@%i kind=%s xdata=%i>" % (
            self.__class__.__name__,
            id(self),
            kind,
            self.xdata,
            )


    @property
    def usr(self):
        return libclang.clang_getCursorUSR(self)


    @property
    def spelling(self):
        return libclang.clang_getCursorSpelling(self)


class CXCompletionChunkKind(c_int):
  CXCompletionChunk_Optional = 0
  CXCompletionChunk_TypedText = 1
  CXCompletionChunk_Text = 2
  CXCompletionChunk_Placeholder = 3
  CXCompletionChunk_Informative = 4
  CXCompletionChunk_CurrentParameter = 5
  CXCompletionChunk_LeftParen = 6
  CXCompletionChunk_RightParen = 7
  CXCompletionChunk_LeftBracket = 8
  CXCompletionChunk_RightBracket = 9
  CXCompletionChunk_LeftBrace = 10
  CXCompletionChunk_RightBrace = 11
  CXCompletionChunk_LeftAngle = 12
  CXCompletionChunk_RightAngle = 13
  CXCompletionChunk_Comma = 14
  CXCompletionChunk_ResultType = 15
  CXCompletionChunk_Colon = 16
  CXCompletionChunk_SemiColon = 17
  CXCompletionChunk_Equal = 18
  CXCompletionChunk_HorizontalSpace = 19
  CXCompletionChunk_VerticalSpace = 20


class CXChildVisitResult(c_int):
  CXChildVisit_Break = 0
  CXChildVisit_Continue = 1
  CXChildVisit_Recurse = 2

CXCursorVisitor = CFUNCTYPE(CXChildVisitResult, CXCursor, CXCursor, CXClientData)

CXCompletionString = c_void_p

class CXCompletionResult(Structure):
    _fields_ = [
        ("CursorKind", CXCursorKind),
        ("CompletionString", CXCompletionString),
        ]


class CXCodeCompleteResults(Structure):
    _fields_ = [
        ("Results" , POINTER(CXCompletionResult)),
        ("NumResults", c_uint),
        ]


class _CXString(Structure):
    # nicked from the original libclang bindings
    """Helper for transforming CXString results."""

    _fields_ = [("spelling", c_char_p), ("free", c_int)]


    def __del__(self):
        libclang.clang_disposeString(self)


    @staticmethod
    def from_result(res, fn, args):
        assert isinstance(res, _CXString)
        return libclang.clang_getCString(res)


def cxstringfunc(argtypes):
    return cfunc(_CXString, argtypes, errcheck=_CXString.from_result)


class libclang(object):

    LIB = None

    @cfunc(CXIndex, [c_int, c_int])
    def clang_createIndex(): pass


    @cfunc(None, [CXIndex])
    def clang_disposeIndex(index) : pass


    @cfunc(CXTranslationUnit, [CXIndex, c_char_p, POINTER(c_char_p), c_int, POINTER(CXUnsavedFile), c_uint, c_uint])
    def clang_parseTranslationUnit(
            index,
            source_filename,
            command_line_args,
            num_command_line_args,
            unsaved_files,
            num_unsaved_files,
            options): pass


    @cfunc(c_int, [CXTranslationUnit, c_uint, POINTER(CXUnsavedFile), c_uint])
    def clang_reparseTranslationUnit(tu, num_unsaved_files, unsaved_files, options):
        pass


    @cfunc(None, [CXTranslationUnit])
    def clang_disposeTranslationUnit(translation_unit): pass


    @cfunc(CXCursor, [CXTranslationUnit])
    def clang_getTranslationUnitCursor(translation_unit): pass


    @cfunc(c_uint, [CXCursor, CXCursorVisitor, CXClientData])
    def clang_visitChildren(parent, visitor, client_data): pass


    @cfunc(c_char_p, [_CXString])
    def clang_getCString(cxstring): pass


    @cfunc(None, [_CXString])
    def clang_disposeString(s): pass


    @cxstringfunc([CXTranslationUnit])
    def clang_getTranslationUnitSpelling(CTUnit): pass


    @cxstringfunc([CXCursor])
    def clang_getCursorUSR(cursor): pass


    @cxstringfunc([CXCursor])
    def clang_getCursorSpelling(cursor): pass


    @cfunc(POINTER(CXCodeCompleteResults),
           [CXTranslationUnit, c_char_p, c_uint, c_uint, POINTER(CXUnsavedFile), c_uint, c_uint])
    def clang_codeCompleteAt(tu, complete_filename, complete_line, complete_column, unsaved_files, num_unsaved_files, options):
        pass


    @cfunc(None, [POINTER(CXCodeCompleteResults)])
    def clang_disposeCodeCompleteResults(results): pass


    @cfunc(None,[POINTER(CXCompletionResult), c_uint])
    def clang_sortCodeCompletionResults(Results, NumResults): pass


    @cfunc(c_uint, [CXCompletionString])
    def clang_getNumCompletionChunks(completion_string): pass


    @cfunc(CXCompletionChunkKind, [CXCompletionString, c_uint])
    def clang_getCompletionChunkKind(completion_string, chunk_num): pass


    @cxstringfunc([CXCompletionString, c_uint])
    def clang_getCompletionChunkText(completion_string, chuck_num): pass


def setup():
    libclang.LIB = CDLL("/usr/local/lib/libclang.dylib")

